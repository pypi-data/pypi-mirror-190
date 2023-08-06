# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

import pickle
from abc import abstractmethod
from typing import Dict

import pandas as pd
import sqlalchemy

from ibm_metrics_plugin.clients.readers.async_query_executor import \
    execute_query
from ibm_metrics_plugin.common.utils.dict_accumulator import merge_two_dicts
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.payload_data_set import \
    PayloadDataSet
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import (
    META_MODEL_SANDBOX_CLASSES, META_MODEL_SANDBOX_MODULES,
    PREDICTED_ACCURACY_BUFFER_LOWER_BOUND,
    PREDICTED_ACCURACY_BUFFER_UPPER_BOUND, MetaModelKind)


class MetaModel:

    def __init__(self, kind: MetaModelKind) -> None:
        self.kind = kind
        self.feature_columns = []
        self.categorical_columns = []
        self.probability_score_columns = []
        self.probability_column = None
        self.is_trained_without_errors = False
        self.is_balanced_data = False
        self.is_optimised = False
        self.categorical_map = {}
        self.errors_map = {}
        self.model_object = None
        self.base_client_accuracy = None
        self.base_predicted_accuracy = None
        self.client_model_metrics = {}

    @classmethod
    def factory(self,
                data: pd.DataFrame,
                data_set: DriftDataSet) -> "MetaModel":
        if isinstance(data, pd.DataFrame):
            # from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_gbt_model import \
            #     GBTMetaModel
            # model = GBTMetaModel()
            from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_hgbt_model import \
                HGBTMetaModel
            model = HGBTMetaModel()
            model.fit(data, data_set)
            return model

    @abstractmethod
    def _prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def _pre_prod_metrics_query(self, data_set: PayloadDataSet) -> str:

        prediction_column = data_set.get_prediction_column().name
        meta_sub_query = None

        if "ibm" in data_set.dialect:
            meta_sub_query = " JSON_VALUE(\"meta\", '$.0' RETURNING VARCHAR(256)) AS \"meta\" "
        elif "postgresql" in data_set.dialect:
            meta_sub_query = " LEFT(RIGHT(\"meta\", -2), -2) AS \"meta\" "
        else:
            raise Exception(
                f"Dialect {data_set.dialect} is not supported. Currently only IBM DB2 and Postgresql are supported.")

        query = f"SELECT payload.\"{prediction_column}\", annotations.\"meta\", COUNT(*) as \"count\" FROM "
        query += f" (SELECT \"{data_set.record_id_column}\", \"{prediction_column}\" FROM \"{data_set.full_table_name}\") as payload "
        query += " inner join "
        query += f" (SELECT \"rid\", {meta_sub_query} FROM \"{data_set.schema_name}\".\"{data_set.table_name}_annotations\" "
        query += f" WHERE \"annotation\" = 'manual_label') as annotations "
        query += f" ON payload.\"{data_set.record_id_column}\" = annotations.\"rid\" "
        query += f" GROUP BY payload.\"{prediction_column}\", annotations.\"meta\" "
        query += f" ORDER BY payload.\"{prediction_column}\", annotations.\"meta\""

        return query

    def predict_proba(self, data: pd.DataFrame) -> pd.Series:
        result_df = self._prepare_data(data)

        probabilities = self.model_object.predict_proba(result_df)
        probabilities = pd.Series(probabilities[:, 0], index=result_df.index)
        return probabilities

    def compute_metrics(self, data: pd.DataFrame, accumulator: Dict = {}) -> Dict:
        result_df = self._prepare_data(data)

        predictions = self.model_object.predict(result_df)

        metrics = {
            "total_records": len(data),
            "total_correct_predictions": sum(predictions)
        }

        return merge_two_dicts(accumulator, metrics)

    async def compute_pre_prod_metrics(self, data: sqlalchemy.engine.base.Engine, data_set: PayloadDataSet) -> Dict:
        query = self._pre_prod_metrics_query(data_set=data_set)

        result = await execute_query(query, data)

        prediction_column = data_set.get_prediction_column().name
        total_records = result["count"].sum()
        total_correct_predictions = result[result[prediction_column]
                                           == result["meta"]]["count"].sum()

        metrics = {
            "total_records": total_records,
            "total_correct_predictions": total_correct_predictions
        }

        return metrics

    def get_accuracy_score(self, raw_metrics: Dict) -> Dict:
        accuracy = raw_metrics["total_correct_predictions"] / raw_metrics["total_records"]

        predicted_accuracy = accuracy + \
            (self.base_client_accuracy -
             self.base_predicted_accuracy)

        # add -0.07 to the predicted accuracy to get min of predicted accuracy range
        # add +0.02 to the predicted accuracy to get max of predicted accuracy range
        predicted_accuracy_range = [predicted_accuracy + PREDICTED_ACCURACY_BUFFER_LOWER_BOUND,
                                    predicted_accuracy + PREDICTED_ACCURACY_BUFFER_UPPER_BOUND]
        # predicted_accuracy is the midpoint of the above range, with 1.0 as the cap.
        predicted_accuracy = min(1.0, sum(predicted_accuracy_range) / 2)

        if predicted_accuracy < accuracy:
            predicted_accuracy = accuracy

        model_quality_drift_score = self.base_client_accuracy - predicted_accuracy
        model_quality_drift_score = max(0, model_quality_drift_score)

        return {
            "predicted_accuracy": predicted_accuracy,
            "model_quality_drift_score": model_quality_drift_score
        }

    def load(self, model_object: object):
        self.model_object = RestrictedUnpickler(model_object).load()

    def to_dict(self) -> Dict:

        dict_ = {
            "kind": self.kind.value,
            "feature_columns": self.feature_columns,
            "categorical_columns": self.categorical_columns,
            "probability_column": self.probability_column,
            "probability_score_columns": self.probability_score_columns,
            "base_client_accuracy": get_python_types(self.base_client_accuracy),
            "base_predicted_accuracy": get_python_types(self.base_predicted_accuracy),
            "categorical_map": get_python_types(self.categorical_map),
            "errors_map": self.errors_map,
            "is_balanced_data": self.is_balanced_data,
            "is_optimised": self.is_optimised,
            "client_model_metrics": self.client_model_metrics
        }

        return dict_

    @classmethod
    def from_dict(cls, dict_: Dict) -> "MetaModel":
        from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_gbt_model import \
            GBTMetaModel
        from ibm_metrics_plugin.metrics.drift_v2.entity.accuracy.sklearn_hgbt_model import \
            HGBTMetaModel

        try:
            model = None
            mm_kind = MetaModelKind(dict_["kind"])
            if mm_kind == MetaModelKind.SKLEARN_GBT:
                model = GBTMetaModel()
            elif mm_kind == MetaModelKind.SKLEARN_HGBT:
                model = HGBTMetaModel()

            model.feature_columns = dict_["feature_columns"]
            model.categorical_columns = dict_["categorical_columns"]
            model.probability_column = dict_["probability_column"]
            model.probability_score_columns = dict_["probability_score_columns"]
            model.base_client_accuracy = dict_["base_client_accuracy"]
            model.base_predicted_accuracy = dict_["base_predicted_accuracy"]
            model.is_balanced_data = dict_["is_balanced_data"]
            model.is_optimised = dict_["is_optimised"]
            model.categorical_map = dict_["categorical_map"]
            model.client_model_metrics = dict_["client_model_metrics"]
            return model
        except KeyError as e:
            raise ValueError(
                f"Cannot create the meta model from the given dictionary. Missing key {e}.") from e


class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes from sandbox.
        if (module in META_MODEL_SANDBOX_MODULES) and (name in META_MODEL_SANDBOX_CLASSES):
            return super(RestrictedUnpickler, self).find_class(module, name)
        # Forbid everything else.
        raise pickle.UnpicklingError(f"'{module}.{name}' is forbidden to load.")
