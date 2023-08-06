# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-H76
# Copyright IBM Corp. 2022
# The source code for this program is not published or other-wise divested of its trade
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from functools import total_ordering
from typing import Dict, List
from uuid import uuid4

from ibm_metrics_plugin.common.utils.datetime_util import DateTimeUtil
from ibm_metrics_plugin.common.utils.metrics_logger import MetricLogger
from ibm_metrics_plugin.common.utils.python_utils import get_python_types
from ibm_metrics_plugin.metrics.drift_v2.entity.column.data_column import \
    DataColumn
from ibm_metrics_plugin.metrics.drift_v2.entity.dataset.data_set import \
    DriftDataSet
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.discrete_statistics import \
    DiscreteStatistics
from ibm_metrics_plugin.metrics.drift_v2.entity.statistics.interval import (
    ContinuousStatisticsInterval, Interval)
from ibm_metrics_plugin.metrics.drift_v2.utils.constants import ColumnRole
from ibm_metrics_plugin.metrics.drift_v2.utils.control_box import \
    ControlBoxManager
from ibm_metrics_plugin.metrics.drift_v2.utils.drift_utils import \
    get_logging_params

logger = MetricLogger(__name__)


@total_ordering
class Insight:
    def __init__(self) -> None:
        self.id = str(uuid4())
        self.display_name = None
        self.source_column = None
        self.source_value = None
        self.insight_score = -1
        self.target_column = None
        self.interval_id = None
        self.baseline_statistics_id = None
        self.production_statistics_id = None
        self.increased_intervals = {}
        self.decreased_intervals = {}

    @property
    def name(self):
        return f"insights_{self.source_column}_{self.source_value}_{self.target_column}"

    @property
    def file_name(self):
        return f"{self.name}.json"

    @classmethod
    def compute(self, baseline_data_set: DriftDataSet,
                production_data_set: DriftDataSet,
                interval: Interval,
                column: DataColumn,
                ) -> List["Insight"]:
        start_time = DateTimeUtil.current_milli_time()
        insights = []

        if isinstance(interval, ContinuousStatisticsInterval):
            value = (interval.lower_bound, interval.upper_bound)
        else:
            value = interval.field
        all_baseline_statistics = baseline_data_set.get_all_statistics(
            column=column, value=value)
        all_production_statistics = production_data_set.get_all_statistics(
            column=column, value=value)

        control_box = ControlBoxManager().get_control_box()

        for name, statistics in all_production_statistics.items():
            insight_start_time = DateTimeUtil.current_milli_time()
            if name not in all_baseline_statistics:
                logger.log_info(
                    f"No baseline statistics found for {column.name}={value}",
                    **get_logging_params(
                        statistics=statistics))
                continue

            baseline_statistics = all_baseline_statistics[name]
            intervals = []

            if isinstance(baseline_statistics, DiscreteStatistics):
                metric_name = control_box.get_default_discrete_feature_drift_metric()
                distances, intervals = baseline_statistics.get_distances(
                    statistics, metric_name=metric_name, return_local_intervals=True)
                score = distances[metric_name.value]

            else:
                target_column = baseline_data_set.get_column(baseline_statistics.target_column)
                if target_column.role in (ColumnRole.PREDICTION, ColumnRole.PROBABILITY_SCORE):
                    metric_name = control_box.get_default_output_drift_metric()
                else:
                    metric_name = control_box.get_default_continuous_feature_drift_metric()

            score = baseline_statistics.get_distances(statistics, metric_name=metric_name)[0]
            threshold = control_box.get_insights_significance_threshold()
            if score < threshold:
                logger.log_info(
                    f"Insight score {score} < {threshold}. Not appending to the list.",
                    **get_logging_params(
                        statistics=statistics,
                        data_set=production_data_set))
                continue

            insight = Insight()
            insight.interval_id = interval.id
            insight.insight_score = score
            insight.source_column = column.name
            insight.source_value = interval.field
            insight.target_column = statistics.target_column
            insight.baseline_statistics_id = baseline_statistics.id
            insight.production_statistics_id = statistics.id

            insight.display_name = f"How did {insight.target_column} distribution change in the interval "
            if isinstance(interval, ContinuousStatisticsInterval):
                insight.display_name += f"{interval.lower_bound} <= {insight.source_column} <= {interval.upper_bound}?"
            else:
                insight.display_name += f"{insight.source_column} = {insight.source_value}?"

            if intervals:
                increased_intervals = sorted(
                    filter(
                        lambda interval: interval.has_increased_in_production(),
                        intervals),
                    reverse=True)
                insight.increased_intervals = {
                    "fields": list(map(lambda interval: interval.field, increased_intervals)),
                    "values": list(
                    map(lambda interval: interval.absolute_change_percentage, increased_intervals))
                }

                decreased_intervals = sorted(
                    filter(
                        lambda interval: ~interval.has_increased_in_production(),
                        intervals),
                    reverse=True)
                insight.decreased_intervals = {
                    "fields": list(map(lambda interval: interval.field, decreased_intervals)),
                    "values": list(
                    map(lambda interval: interval.absolute_change_percentage, decreased_intervals))
                }

            insights.append(insight)
            logger.log_debug(
                "Insight added",
                **get_logging_params(
                    insight=insight,
                    start_time=insight_start_time))

        logger.log_info(
            f"{len(insights)} added",
            **get_logging_params(
                column=column,
                data_set=production_data_set,
                start_time=start_time))
        return insights

    def __lt__(self, other) -> bool:
        return self.insight_score < other.insight_score

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        return self.insight_score == other.insight_score

    def to_dict(self) -> Dict:

        return {
            "id": get_python_types(self.id),
            "name": self.name,
            "display_name": self.display_name,
            "insight_score": get_python_types(self.insight_score),
            "target_column": self.target_column,
            "source_column": self.source_column,
            "source_value": get_python_types(self.source_value),
            "interval_id": get_python_types(self.interval_id),
            "baseline_statistics_id": get_python_types(self.baseline_statistics_id),
            "production_statistics_id": get_python_types(self.production_statistics_id),
            "increased_intervals": get_python_types(self.increased_intervals),
            "decreased_intervals": get_python_types(self.decreased_intervals)
        }