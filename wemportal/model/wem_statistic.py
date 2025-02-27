# pylint: disable=too-few-public-methods
"""
Classes for statistics management
"""
from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import List, Dict
from dateutil import parser


class StatisticType(IntEnum):
    """
    Energy type for statistics
    """
    heating = 1
    hot_water = 2
    summary = 3


class GraphType(IntEnum):
    """
    Time period for statistics
    """
    daily = 0
    monthly = 1
    yearly = 2


@dataclass
class StatisticValue():
    """Manage statistic values"""
    datetime: datetime
    value: float


@dataclass
class WemStatistic():
    """Manage statistics with values"""
    statistics_type: StatisticType
    graph_type: GraphType
    has_data: bool
    max_date: datetime
    min_date: datetime
    unit: str
    values: List[StatisticValue]


@dataclass
class WemHeatingStatistic(WemStatistic):
    """Manage statistics with values for heating system"""
    statistics_type = StatisticType.heating


@dataclass
class WemHotWaterStatistic(WemStatistic):
    """Manage statistics with values for hot water system"""
    statistics_type = StatisticType.hot_water


class StatisticValueParser:
    """Parser for statistic values"""
    @staticmethod
    def load(value: Dict) -> StatisticValue:
        """load object from dict"""
        return StatisticValue(
            datetime= parser.parse(value["Date"]),
            value = value["Value"]
        )


class WemHeatingStatisticParser:
    """Parser for statistics with values for heating system"""
    @staticmethod
    def load(statistic: Dict, graph_type: GraphType) -> WemHeatingStatistic:
        """load object from dict"""
        return WemHeatingStatistic(
            statistics_type = StatisticType.heating,
            graph_type = graph_type,
            has_data = statistic["HasData"],
            max_date = parser.parse(statistic["MaxDate"]),
            min_date = parser.parse(statistic["MinDate"]),
            unit = statistic["Unit"],
            values = [StatisticValueParser.load(value) for value in statistic["Data"]]
        )


class WemHotWaterStatisticParser:
    """Parser for statistics with values for hot water system"""
    @staticmethod
    def load(statistic: Dict, graph_type: GraphType) -> WemHotWaterStatistic:
        """load object from dict"""
        return WemHotWaterStatistic(
            statistics_type = StatisticType.hot_water,
            graph_type = graph_type,
            has_data = statistic["HasData"],
            max_date = parser.parse(statistic["MaxDate"]),
            min_date = parser.parse(statistic["MinDate"]),
            unit = statistic["Unit"],
            values = [StatisticValueParser.load(value) for value in statistic["Data"]]
        )
