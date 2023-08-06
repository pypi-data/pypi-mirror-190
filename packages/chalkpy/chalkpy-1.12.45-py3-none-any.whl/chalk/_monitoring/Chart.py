import dataclasses
import zlib
from copy import deepcopy
from enum import Enum
from typing import Callable, ClassVar, List, Literal, Optional, Set, Tuple, TypeVar, Union, overload

from chalk import Resolver
from chalk.features import FeatureWrapper
from chalk.utils.duration import parse_chalk_duration

T = TypeVar("T")


class MetricKind(str, Enum):
    FEATURE_REQUEST_COUNT = "FEATURE_REQUEST_COUNT"
    FEATURE_LATENCY = "FEATURE_LATENCY"
    FEATURE_STALENESS = "FEATURE_STALENESS"
    FEATURE_VALUE = "FEATURE_VALUE"
    FEATURE_WRITE = "FEATURE_WRITE"
    FEATURE_NULL_RATIO = "FEATURE_NULL_RATIO"

    RESOLVER_REQUEST_COUNT = "RESOLVER_REQUEST_COUNT"
    RESOLVER_LATENCY = "RESOLVER_LATENCY"
    RESOLVER_SUCCESS_RATIO = "RESOLVER_SUCCESS_RATIO"

    QUERY_COUNT = "QUERY_COUNT"
    QUERY_LATENCY = "QUERY_LATENCY"
    QUERY_SUCCESS_RATIO = "QUERY_SUCCESS_RATIO"

    BILLING_INFERENCE = "BILLING_INFERENCE"
    BILLING_CRON = "BILLING_CRON"
    BILLING_MIGRATION = "BILLING_MIGRATION"

    CRON_COUNT = "CRON_COUNT"
    CRON_LATENCY = "CRON_LATENCY"

    STREAM_MESSAGES_PROCESSED = "STREAM_MESSAGES_PROCESSED"
    STREAM_MESSAGE_LATENCY = "STREAM_MESSAGE_LATENCY"

    STREAM_WINDOWS_PROCESSED = "STREAM_WINDOWS_PROCESSED"
    STREAM_WINDOW_LATENCY = "STREAM_WINDOW_LATENCY"


class FilterKind(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    FEATURE_TAG = "FEATURE_TAG"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"
    RESOLVER_TAG = "RESOLVER_TAG"

    CRON_STATUS = "CRON_STATUS"
    MIGRATION_STATUS = "MIGRATION_STATUS"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"
    OPERATION_ID = "OPERATION_ID"

    QUERY_NAME = "QUERY_NAME"
    QUERY_STATUS = "QUERY_STATUS"

    IS_NULL = "IS_NULL"


ResolverType = Literal["online", "offline", "stream"]
FeatureNameType = Union[FeatureWrapper, str]
ResolverNameType = Union[Resolver, str]


class ComparatorKind(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    ONE_OF = "ONE_OF"


class WindowFunctionKind(str, Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"

    PERCENTILE_99 = "PERCENTILE_99"
    PERCENTILE_95 = "PERCENTILE_95"
    PERCENTILE_75 = "PERCENTILE_75"
    PERCENTILE_50 = "PERCENTILE_50"
    PERCENTILE_25 = "PERCENTILE_25"
    PERCENTILE_5 = "PERCENTILE_5"

    ALL_PERCENTILES = "ALL_PERCENTILES"

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__


class GroupByKind(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    IS_NULL = "IS_NULL"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"

    QUERY_STATUS = "QUERY_STATUS"
    QUERY_NAME = "QUERY_NAME"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"


class MetricFormulaKind(str, Enum):
    SUM = "SUM"
    TOTAL_RATIO = "TOTAL_RATIO"
    RATIO = "RATIO"
    PRODUCT = "PRODUCT"
    ABS = "ABS"
    KS_STAT = "KS_STAT"
    KS_TEST = "KS_TEST"
    KS_THRESHOLD = "KS_THRESHOLD"
    TIME_OFFSET = "TIME_OFFSET"


class AlertSeverityKind(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ThresholdPosition(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"


class ChartLinkKind(str, Enum):
    resolver = "resolver"
    feature = "feature"
    query = "query"
    manual = "manual"


@dataclasses.dataclass
class MetricFilter:
    kind: FilterKind
    comparator: ComparatorKind
    value: List[str]


@dataclasses.dataclass
class ThresholdFunction:
    lhs: "Series"
    operation: str
    rhs: float


@dataclasses.dataclass
class SingleSeriesOperand:
    operand: int


@dataclasses.dataclass
class MultiSeriesOperand:
    operands: List[int]


@dataclasses.dataclass
class DatasetFeatureOperand:
    dataset: str
    feature: str


class Series:
    def __init__(
        self,
        name: str,
        metric: Union[MetricKind, str],
        window_function: Optional[Union[WindowFunctionKind, str]] = None,
        time_shift: Optional[int] = None,
    ):
        self._name = name
        self._metric = MetricKind(metric.upper()) if metric else None
        self._filters: List[MetricFilter] = []
        if window_function:
            if WindowFunctionKind.has_member_key(window_function.upper()):
                window_function_kind = WindowFunctionKind(window_function.upper())
            else:
                window_function_kind = self._get_window_function_type(window_function.upper())
                if not window_function_kind:
                    raise ValueError(f"'window_function' value '{window_function}' 'invalid for WindowFunctionKind")
        else:
            window_function_kind = None
        self._window_function = window_function_kind
        self._group_by: List[GroupByKind] = []
        self._time_shift = time_shift
        self._entity_kind = ChartLinkKind.manual
        self._entity_id = None

    @staticmethod
    def _get_window_function_type(key: str) -> Union[WindowFunctionKind, None]:
        window_function_value_dict = {
            "99%": WindowFunctionKind.PERCENTILE_99,
            "95%": WindowFunctionKind.PERCENTILE_95,
            "75%": WindowFunctionKind.PERCENTILE_75,
            "50%": WindowFunctionKind.PERCENTILE_50,
            "25%": WindowFunctionKind.PERCENTILE_25,
            "5%": WindowFunctionKind.PERCENTILE_5,
            "99": WindowFunctionKind.PERCENTILE_99,
            "95": WindowFunctionKind.PERCENTILE_95,
            "75": WindowFunctionKind.PERCENTILE_75,
            "50": WindowFunctionKind.PERCENTILE_50,
            "25": WindowFunctionKind.PERCENTILE_25,
            "5": WindowFunctionKind.PERCENTILE_5,
            "ALL": WindowFunctionKind.ALL_PERCENTILES,
        }
        return window_function_value_dict.get(key)

    @staticmethod
    def _get_filter_string_type(key: str) -> Union[FilterKind, None]:
        string_dict = {
            "feature_tag": FilterKind.FEATURE_TAG,
            "resolver_tag": FilterKind.RESOLVER_TAG,
            "operation_id": FilterKind.OPERATION_ID,
            "query_name": FilterKind.QUERY_NAME,
        }
        return string_dict.get(key)

    @staticmethod
    def _get_filter_status_type(key: str) -> Union[FilterKind, None]:
        status_dict = {
            "feature": FilterKind.FEATURE_STATUS,
            "resolver": FilterKind.RESOLVER_STATUS,
            "cron": FilterKind.CRON_STATUS,
            "migration": FilterKind.MIGRATION_STATUS,
            "query": FilterKind.QUERY_STATUS,
        }
        return status_dict.get(key)

    def where(
        self,
        feature: Optional[Union[List[FeatureNameType], FeatureNameType]] = None,
        resolver: Optional[Union[List[ResolverNameType], ResolverNameType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
        cron_status: Optional[Literal["success", "failure"]] = None,
        migration_status: Optional[Literal["success", "failure"]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        cache_hit: Optional[bool] = None,
        is_null: Optional[bool] = None,
    ) -> "Series":
        return self._where(
            feature_name=feature,
            resolver_name=resolver,
            feature_tag=feature_tag,
            resolver_tag=resolver_tag,
            operation_id=operation_id,
            query_name=query_name,
            feature_status=feature_status,
            resolver_status=resolver_status,
            cron_status=cron_status,
            migration_status=migration_status,
            query_status=query_status,
            resolver_type=resolver_type,
            cache_hit=cache_hit,
            is_null=is_null,
            equals=True,
        )

    def where_not(
        self,
        feature: Optional[Union[List[FeatureNameType], Union[FeatureWrapper, str]]] = None,
        resolver: Optional[Union[List[ResolverNameType], ResolverNameType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
        cron_status: Optional[Literal["success", "failure"]] = None,
        migration_status: Optional[Literal["success", "failure"]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        cache_hit: Optional[bool] = None,
        is_null: Optional[bool] = None,
    ) -> "Series":
        return self._where(
            feature_name=feature,
            resolver_name=resolver,
            feature_tag=feature_tag,
            resolver_tag=resolver_tag,
            operation_id=operation_id,
            query_name=query_name,
            feature_status=feature_status,
            resolver_status=resolver_status,
            cron_status=cron_status,
            migration_status=migration_status,
            query_status=query_status,
            resolver_type=resolver_type,
            cache_hit=cache_hit,
            is_null=is_null,
            equals=False,
        )

    def _where(
        self,
        feature_name: Optional[Union[List[FeatureNameType], Union[FeatureWrapper, str]]] = None,
        resolver_name: Optional[Union[List[ResolverNameType], ResolverNameType]] = None,
        feature_tag: Optional[Union[List[str], str]] = None,
        resolver_tag: Optional[Union[List[str], str]] = None,
        operation_id: Optional[Union[List[str], str]] = None,
        query_name: Optional[Union[List[str], str]] = None,
        feature_status: Optional[Literal["success", "failure"]] = None,
        resolver_status: Optional[Literal["success", "failure"]] = None,
        cron_status: Optional[Literal["success", "failure"]] = None,
        migration_status: Optional[Literal["success", "failure"]] = None,
        query_status: Optional[Literal["success", "failure"]] = None,
        resolver_type: Optional[Union[List[ResolverType], ResolverType]] = None,
        cache_hit: Optional[bool] = None,
        is_null: Optional[bool] = None,
        equals: Optional[bool] = True,
    ) -> "Series":
        copy = self._copy_with()
        success_dict = {"success": True, "failure": False}
        if feature_name:
            feature_name = [feature_name] if not isinstance(feature_name, list) else feature_name
            copy = copy._feature_name_filter(*feature_name, equals=equals)
        if resolver_name:
            resolver_name = [resolver_name] if not isinstance(resolver_name, list) else resolver_name
            copy = copy._resolver_name_filter(*resolver_name, equals=equals)
        if feature_tag:
            feature_tag = [feature_tag] if isinstance(feature_tag, str) else feature_tag
            copy = copy._string_filter(*feature_tag, kind="feature_tag", equals=equals)
        if resolver_tag:
            resolver_tag = [resolver_tag] if isinstance(resolver_tag, str) else resolver_tag
            copy = copy._string_filter(*resolver_tag, kind="resolver_tag", equals=equals)
        if operation_id:
            operation_id = [operation_id] if isinstance(operation_id, str) else operation_id
            copy = copy._string_filter(*operation_id, kind="operation_id", equals=equals)
        if query_name:
            query_name = [query_name] if isinstance(query_name, str) else query_name
            copy = copy._string_filter(*query_name, kind="query_name", equals=equals)
        if feature_status:
            copy = copy._status_filter(kind="feature", success=success_dict[feature_status] == equals)
        if resolver_status:
            copy = copy._status_filter(kind="resolver", success=success_dict[resolver_status] == equals)
        if cron_status:
            copy = copy._status_filter(kind="cron", success=success_dict[cron_status] == equals)
        if migration_status:
            copy = copy._status_filter(kind="migration", success=success_dict[migration_status] == equals)
        if query_status:
            copy = copy._status_filter(kind="query", success=success_dict[query_status] == equals)
        if resolver_type:
            resolver_type = [resolver_type] if not isinstance(resolver_type, list) else resolver_type
            copy = copy.with_resolver_type_filter(*resolver_type, equals=equals)
        if cache_hit is not None:
            copy = copy._true_false_filter(kind="cache_hit", value=equals)
        if is_null is not None:
            copy = copy._true_false_filter(kind="null", value=equals)
        return copy

    def with_feature_name_filter(self, *features: Tuple[FeatureNameType]) -> "Series":
        return self._feature_name_filter(*features, equals=True)

    def without_feature_name_filter(self, *features: Tuple[FeatureNameType]) -> "Series":
        return self._feature_name_filter(*features, equals=False)

    def _feature_name_filter(self, *features: Tuple[FeatureNameType], equals: bool) -> "Series":
        if not features:
            raise ValueError(f"One or more Chalk Features must be supplied.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(features) == 1 or not equals:
            for feature in features:
                value = str(feature) if isinstance(feature, FeatureWrapper) else feature
                metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(features) == 1:
                feature = features[0]
                copy._entity_id = value = str(feature) if isinstance(feature, FeatureWrapper) else feature
                copy._entity_kind = ChartLinkKind.feature
        else:
            value = [str(feature) if isinstance(feature, FeatureWrapper) else feature for feature in features]
            metric_filter = MetricFilter(kind=FilterKind.FEATURE_NAME, comparator=ComparatorKind.ONE_OF, value=value)
            copy._filters.append(metric_filter)
        return copy

    def with_resolver_name_filter(self, *resolvers: Tuple[ResolverNameType]) -> "Series":
        return self._resolver_name_filter(*resolvers, equals=True)

    def without_resolver_name_filter(self, *resolvers: Tuple[ResolverNameType]) -> "Series":
        return self._resolver_name_filter(*resolvers, equals=False)

    def _resolver_name_filter(self, *resolvers: Tuple[ResolverNameType], equals: bool) -> "Series":
        if not resolvers:
            raise ValueError(f"One or more Chalk Resolvers must be supplied.")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolvers) == 1 or not equals:
            for resolver in resolvers:
                value = resolver.fqn if isinstance(resolver, Resolver) else resolver
                metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=comparator, value=[value])
                copy._filters.append(metric_filter)
            if len(resolvers) == 1:
                resolver = resolvers[0]
                copy._entity_id = resolver.fqn if isinstance(resolver, Resolver) else resolver
                copy._entity_kind = ChartLinkKind.resolver
        else:
            value = [resolver.fqn if isinstance(resolver, Resolver) else resolver for resolver in resolvers]
            metric_filter = MetricFilter(kind=FilterKind.RESOLVER_NAME, comparator=ComparatorKind.ONE_OF, value=value)
            copy._filters.append(metric_filter)
        return copy

    def with_feature_tag_filter(self, *tags: Tuple[str]) -> "Series":
        return self._string_filter(*tags, kind="feature_tag", equals=True)

    def without_feature_tag_filter(self, *tags: Tuple[str]) -> "Series":
        return self._string_filter(*tags, kind="feature_tag", equals=False)

    def with_resolver_tag_filter(self, *tags: Tuple[str]) -> "Series":
        return self._string_filter(*tags, kind="resolver_tag", equals=True)

    def without_resolver_tag_filter(self, *tags: Tuple[str]) -> "Series":
        return self._string_filter(*tags, kind="resolver_tag", equals=False)

    def with_operation_id_filter(self, *operation_ids: Tuple[str]) -> "Series":
        return self._string_filter(*operation_ids, kind="operation_id", equals=True)

    def without_operation_id_filter(self, *operation_ids: Tuple[str]) -> "Series":
        return self._string_filter(*operation_ids, kind="operation_id", equals=False)

    def with_query_name_filter(self, *query_names: Tuple[str]) -> "Series":
        return self._string_filter(*query_names, kind="query_name", equals=True)

    def without_query_name_filter(self, *query_names: Tuple[str]) -> "Series":
        return self._string_filter(*query_names, kind="query_name", equals=False)

    def _string_filter(self, *strings: Tuple[str], kind: str, equals=True):
        if not strings:
            raise ValueError(f"One or more arguments must be supplied for this filter")
        copy = self._copy_with()
        filter_kind = self._get_filter_string_type(kind)
        if not filter_kind:
            raise ValueError(f"no filter for '{kind}' found")
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(strings) == 1 or not equals:
            for string in strings:
                metric_filter = MetricFilter(kind=filter_kind, comparator=comparator, value=[string])
                copy._filters.append(metric_filter)
            if len(strings) == 1 and kind == "query_name":
                copy._entity_id = strings[0]
                copy._entity_kind = ChartLinkKind.query
        else:
            metric_filter = MetricFilter(kind=filter_kind, comparator=ComparatorKind.ONE_OF, value=list(strings))
            copy._filters.append(metric_filter)
        return copy

    def with_resolver_type_filter(
        self, *resolver_types: Tuple[Literal["online", "offline", "stream"]], equals=True
    ) -> "Series":
        if not resolver_types:
            raise ValueError(f"One or more resolver types from 'online', 'offline', or 'stream' must be supplied")
        if not set(resolver_types).issubset(["online", "offline", "stream"]):
            raise ValueError(f"Resolver types '{resolver_types}' must be one of 'online', 'offline', or 'stream'")
        copy = self._copy_with()
        comparator = ComparatorKind.EQ if equals else ComparatorKind.NEQ
        if len(resolver_types) == 1 or not equals:
            for resolver_type in resolver_types:
                metric_filter = MetricFilter(
                    kind=FilterKind.ONLINE_OFFLINE, comparator=comparator, value=[resolver_type]
                )
                copy._filters.append(metric_filter)
        else:
            metric_filter = MetricFilter(
                kind=FilterKind.ONLINE_OFFLINE, comparator=ComparatorKind.ONE_OF, value=list(resolver_types)
            )
            copy._filters.append(metric_filter)
        return copy

    def with_null_filter(self) -> "Series":
        return self._true_false_filter(kind="null", value=True)

    def without_null_filter(self) -> "Series":
        return self._true_false_filter(kind="null", value=False)

    def with_cache_hit_filter(self) -> "Series":
        return self._true_false_filter(kind="cache_hit", value=True)

    def without_cache_hit_filter(self) -> "Series":
        return self._true_false_filter(kind="cache_hit", value=False)

    def _true_false_filter(self, kind: str, value: bool) -> "Series":
        copy = self._copy_with()
        filter_kind = FilterKind.IS_NULL if kind == "null" else FilterKind.CACHE_HIT
        value = "true" if value else "false"
        metric_filter = MetricFilter(kind=filter_kind, comparator=ComparatorKind.EQ, value=[value])
        copy._filters.append(metric_filter)
        return copy

    def with_feature_status_filter(self, success=True) -> "Series":
        return self._status_filter(kind="feature", success=success)

    def with_resolver_status_filter(self, success=True) -> "Series":
        return self._status_filter(kind="resolver", success=success)

    def with_cron_status_filter(self, success=True) -> "Series":
        return self._status_filter(kind="cron", success=success)

    def with_query_status_filter(self, success=True) -> "Series":
        return self._status_filter(kind="query", success=success)

    def _status_filter(self, kind: str, success: bool) -> "Series":
        copy = self._copy_with()
        value = "success" if success else "failure"
        filter_kind = self._get_filter_status_type(kind)
        if not filter_kind:
            raise ValueError(f"no status filter for '{kind}' found")
        metric_filter = MetricFilter(kind=filter_kind, comparator=ComparatorKind.EQ, value=[value])
        copy._filters.append(metric_filter)
        return copy

    def with_filter(
        self, kind: Union[FilterKind, str], comparator: Union[ComparatorKind, str], value: Union[List[str], str]
    ) -> "Series":
        copy = self._copy_with()
        kind = FilterKind(kind.upper())
        comparator = ComparatorKind(comparator.upper())
        value = [value] if isinstance(value, str) else value
        metric_filter = MetricFilter(kind=kind, comparator=comparator, value=value)
        copy._filters.append(metric_filter)
        return copy

    def with_window_function(self, window_function: Union[WindowFunctionKind, str]) -> "Series":

        copy = self._copy_with()
        copy._window_function = WindowFunctionKind(window_function.upper())
        return copy

    def with_group_by(self, group_by: Union[GroupByKind, str]) -> "Series":
        copy = self._copy_with()
        group_by = GroupByKind(group_by.upper())
        copy._group_by.append(group_by)
        return copy

    def with_group_by_feature_status(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_STATUS)
        return copy

    def with_group_by_feature_name(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.FEATURE_NAME)
        return copy

    def with_group_by_is_null(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.IS_NULL)
        return copy

    def with_group_by_resolver_status(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_STATUS)
        return copy

    def with_group_by_resolver_name(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.RESOLVER_NAME)
        return copy

    def with_group_by_query_status(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_STATUS)
        return copy

    def with_group_by_query_name(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.QUERY_NAME)
        return copy

    def with_group_by_resolver_type(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.ONLINE_OFFLINE)
        return copy

    def with_group_by_cache_hit(self) -> "Series":
        copy = self._copy_with()
        copy._group_by.append(GroupByKind.CACHE_HIT)
        return copy

    def with_time_shift(self, time_shift: int) -> "Series":
        copy = self._copy_with()
        copy._time_shift = time_shift
        return copy

    def _copy_with(self) -> "Series":
        self_copy = deepcopy(self)
        return self_copy

    def __gt__(self, other) -> ThresholdFunction:
        return ThresholdFunction(self, ">", other)

    def __lt__(self, other) -> ThresholdFunction:
        return ThresholdFunction(self, "<", other)

    def __str__(self) -> str:
        return f"Series(name='{self._name}')"

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        metric = str(self._metric) if self._metric else "."
        filter_strings = (
            sorted([f"{f.kind}.{f.comparator}.{'.'.join(f.value)}" for f in self._filters]) if self._filters else "."
        )
        window_function = str(self._window_function) if self._window_function else "."
        group_by = sorted([str(group_by) for group_by in self._group_by]) if self._group_by else "."
        time_shift = str(self._time_shift) if self._time_shift else "."

        series_string = (
            f"series.{name}.{metric}.{'.'.join(filter_strings)}.{window_function}.{'.'.join(group_by)}.{time_shift}"
        )

        return zlib.crc32(series_string.encode())


class Formula:
    def __init__(
        self,
        name: Optional[str] = None,
        kind: Optional[Union[MetricFormulaKind, str]] = None,
        operands: Optional[Union[SingleSeriesOperand, MultiSeriesOperand, DatasetFeatureOperand]] = None,
    ):
        self._name = name
        self._kind = MetricFormulaKind(kind.upper()) if kind else None
        self._operands = operands

    def with_name(self, name: str) -> "Formula":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_kind(self, kind: Union[MetricFormulaKind, str]) -> "Formula":
        copy = self._copy_with()
        copy._kind = MetricFormulaKind(kind.upper())
        return copy

    def with_operands(
        self, operands: Union[SingleSeriesOperand, MultiSeriesOperand, DatasetFeatureOperand]
    ) -> "Formula":
        copy = self._copy_with()
        copy._operands = operands
        return copy

    def _copy_with(self) -> "Formula":
        self_copy = deepcopy(self)
        return self_copy

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        kind = str(self._kind) if self._kind else "."
        operands = ""
        if isinstance(self._operands, SingleSeriesOperand):
            operands = self._operands.operand
        elif isinstance(self._operands, MultiSeriesOperand):
            operands = self._operands.operands
        elif isinstance(self._operands, DatasetFeatureOperand):
            operands = f"{self._operands.dataset}.{self._operands.feature}"

        formula_string = f"formula.{name}.{kind}.{operands}"

        return zlib.crc32(formula_string.encode())


class Trigger:
    def __init__(
        self,
        name: str,
        severity: Optional[Union[AlertSeverityKind, str]] = None,
        threshold_position: Optional[Union[ThresholdPosition, str]] = None,
        threshold_value: Optional[float] = None,
        series_name: Optional[str] = None,
        channel_name: Optional[str] = None,
    ):
        self._name = name
        self._severity = severity
        self._threshold_position = threshold_position
        self._threshold_value = threshold_value
        self._series_name = series_name
        self._channel_name = channel_name

    def with_name(self, name: str) -> "Trigger":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_severity(self, severity: Union[AlertSeverityKind, str]) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind(severity.upper())
        return copy

    def with_critical_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.CRITICAL
        return copy

    def with_error_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.ERROR
        return copy

    def with_warning_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.WARNING
        return copy

    def with_info_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.INFO
        return copy

    def with_threshold_position(self, threshold_position: Union[ThresholdPosition, str]) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_position = ThresholdPosition(threshold_position.upper())
        return copy

    def with_threshold_value(self, threshold_value: float) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_value = threshold_value
        return copy

    def with_series_name(self, series_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._series_name = series_name
        return copy

    def with_channel_name(self, channel_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._channel_name = channel_name
        return copy

    def _copy_with(self) -> "Trigger":
        self_copy = deepcopy(self)
        return self_copy

    def __str__(self) -> str:
        return f"Trigger(name='{self._name}')"

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        severity = str(self._severity) if self._severity else "."
        threshold_position = str(self._threshold_position) if self._threshold_position else "."
        threshold_value = str(self._threshold_value) if self._threshold_value else "."
        series_name = self._series_name if self._series_name else "."
        channel_name = self._channel_name if self._channel_name else "."

        trigger_string = (
            f"trigger.{name}.{severity}.{threshold_position}." f"{threshold_value}.{series_name}.{channel_name}"
        )

        return zlib.crc32(trigger_string.encode())


def _copy_with(function: Callable):
    def inner(self, *args, **kwargs):
        copy = deepcopy(self)
        if not self._keep:
            if self in Chart._registry:
                Chart._registry.remove(self)
        return_copy = function(copy, *args, **kwargs)
        Chart._registry.add(return_copy)
        return return_copy

    return inner


# MetricConfigGQL
class Chart:
    _registry: ClassVar[Set[Union[str, "Chart"]]] = set()

    def __init__(self, name: str, window_period: Optional[str] = None, keep: Optional[bool] = False):
        self._name = name
        self._window_period = window_period
        self._series: List[Series] = []
        self._formulas: List[Formula] = []
        self._trigger = None
        self._keep = keep
        self._entity_id = None
        self._entity_kind = ChartLinkKind.manual
        Chart._registry.add(self)

    @_copy_with
    def with_window_period(self, window_period: str) -> "Chart":
        parse_chalk_duration(window_period)
        self._window_period = window_period
        return self

    def with_feature_request_count_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.FEATURE_REQUEST_COUNT,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_feature_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.FEATURE_LATENCY, window_function=window_function, time_shift=time_shift
        )

    def with_feature_staleness_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.FEATURE_STALENESS,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_feature_value_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.FEATURE_VALUE, window_function=window_function, time_shift=time_shift
        )

    def with_feature_write_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.FEATURE_WRITE, window_function=window_function, time_shift=time_shift
        )

    def with_feature_null_ratio_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.FEATURE_NULL_RATIO,
            time_shift=time_shift,
        )

    def with_resolver_request_count_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.RESOLVER_REQUEST_COUNT,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_resolver_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.RESOLVER_LATENCY, window_function=window_function, time_shift=time_shift
        )

    def with_resolver_success_ratio_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.RESOLVER_SUCCESS_RATIO,
            time_shift=time_shift,
        )

    def with_query_count_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.QUERY_COUNT, window_function=window_function, time_shift=time_shift
        )

    def with_query_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.QUERY_LATENCY, window_function=window_function, time_shift=time_shift
        )

    def with_query_success_ratio_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.QUERY_SUCCESS_RATIO,
            time_shift=time_shift,
        )

    def with_billing_inference_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.BILLING_INFERENCE,
            time_shift=time_shift,
        )

    def with_billing_cron_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(name=series_name, metric=MetricKind.BILLING_CRON, time_shift=time_shift)

    def with_billing_migration_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.BILLING_MIGRATION,
            time_shift=time_shift,
        )

    def with_cron_count_series(self, series_name: str, time_shift: Optional[int] = None) -> "Chart":
        return self.with_series(name=series_name, metric=MetricKind.CRON_COUNT, time_shift=time_shift)

    def with_cron_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name, metric=MetricKind.CRON_LATENCY, window_function=window_function, time_shift=time_shift
        )

    def with_stream_messages_processed_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.STREAM_MESSAGES_PROCESSED,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_stream_message_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.STREAM_MESSAGE_LATENCY,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_stream_windows_processed_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.STREAM_WINDOWS_PROCESSED,
            window_function=window_function,
            time_shift=time_shift,
        )

    def with_stream_window_latency_series(
        self, series_name: str, window_function: Union[WindowFunctionKind, str], time_shift: Optional[int] = None
    ) -> "Chart":
        return self.with_series(
            name=series_name,
            metric=MetricKind.STREAM_WINDOW_LATENCY,
            window_function=window_function,
            time_shift=time_shift,
        )

    @overload
    def with_series(self, /, series: Series, **kwargs) -> "Chart":
        ...

    @overload
    def with_series(self, /, name: str, **kwargs) -> "Chart":
        ...

    @_copy_with
    def with_series(self, /, name: Optional[str] = None, series: Optional[Series] = None, **kwargs) -> "Chart":
        if series:
            if not isinstance(series, Series):
                raise ValueError(f"'series' value '{series}' must be a Series object")
            self._series.append(series)
            if series._entity_id:
                self._entity_id = series._entity_id
                self._entity_kind = series._entity_kind
            return self
        if name:
            if not isinstance(name, str):
                raise ValueError(f"'name' value '{name}' must be a string")
            new_series = Series(name=name, **kwargs)
            self._series.append(new_series)
            return self
        raise ValueError("Either a 'name' for a new series or an existing Series 'series' must be supplied")

    def get_series(self, series_name: str) -> Series:
        for series in self._series:
            if series._name == series_name:
                return series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    def _get_series_index(self, series_name: str) -> Tuple[int, Series]:
        for i, series in enumerate(self._series):
            if series._name == series_name:
                return i, series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    @overload
    def with_formula(self, /, formula: Formula, **kwargs) -> "Chart":
        ...

    @overload
    def with_formula(self, /, name: str, **kwargs) -> "Chart":
        ...

    @_copy_with
    def with_formula(self, /, name: Optional[str] = None, formula: Optional[Formula] = None, **kwargs) -> "Chart":
        if formula:
            if not isinstance(formula, Formula):
                raise ValueError(f"'formula' value '{formula}' must be a Formula object")
            self._formulas.append(formula)
            return self
        if name:
            if not isinstance(name, str):
                raise ValueError(f"'name' value '{name}' must be a string")
            new_formula = Formula(**kwargs)
            self._formulas.append(new_formula)
            return self
        raise ValueError("Either a 'name' for a new formula or an existing Formula 'formula' must be supplied")

    @_copy_with
    def with_trigger(
        self,
        expression: ThresholdFunction,
        trigger_name: str,
        severity: Optional[Union[AlertSeverityKind, str]] = None,
        channel_name: Optional[str] = None,
    ) -> "Chart":
        if not isinstance(expression.lhs, Series):
            raise ValueError(f"Left hand side of expression '{expression.lhs}' must be a Series")
        threshold_position = ThresholdPosition.ABOVE if expression.operation == ">" else ThresholdPosition.BELOW
        trigger = Trigger(
            name=trigger_name,
            severity=AlertSeverityKind(severity.upper()),
            threshold_position=threshold_position,
            threshold_value=expression.rhs,
            series_name=expression.lhs._name,
            channel_name=channel_name,
        )
        self._trigger = trigger
        return self

    @_copy_with
    def with_feature_name_filter(
        self,
        *features: Tuple[FeatureNameType],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_feature_name_filter(*features)
        return self

    @_copy_with
    def without_feature_name_filter(
        self,
        *features: Tuple[FeatureNameType],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_feature_name_filter(*features)
        return self

    @_copy_with
    def with_resolver_name_filter(
        self,
        *resolvers: Tuple[ResolverNameType],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_resolver_name_filter(*resolvers)
        return self

    @_copy_with
    def without_resolver_name_filter(
        self,
        *resolvers: Tuple[ResolverNameType],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_resolver_name_filter(*resolvers)
        return self

    @_copy_with
    def with_feature_tag_filter(
        self,
        *tags: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_feature_tag_filter(*tags)
        return self

    @_copy_with
    def without_feature_tag_filter(
        self,
        *tags: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_feature_tag_filter(*tags)
        return self

    @_copy_with
    def with_resolver_tag_filter(
        self,
        *tags: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_resolver_tag_filter(*tags)
        return self

    @_copy_with
    def without_resolver_tag_filter(
        self,
        *tags: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_resolver_tag_filter(*tags)
        return self

    @_copy_with
    def with_operation_id_filter(
        self,
        *operation_ids: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_operation_id_filter(*operation_ids)
        return self

    @_copy_with
    def without_operation_id_filter(
        self,
        *operation_ids: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_operation_id_filter(*operation_ids)
        return self

    @_copy_with
    def with_resolver_type_filter(
        self,
        *resolver_types: Tuple[str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_resolver_type_filter(*resolver_types)
        return self

    @_copy_with
    def with_null_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_null_filter()
        return self

    @_copy_with
    def without_null_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_null_filter()
        return self

    @_copy_with
    def with_cache_hit_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_cache_hit_filter()
        return self

    @_copy_with
    def without_cache_hit_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.without_cache_hit_filter()
        return self

    @_copy_with
    def with_feature_status_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_feature_status_filter()
        return self

    @_copy_with
    def with_resolver_status_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_resolver_status_filter()
        return self

    @_copy_with
    def with_cron_status_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_cron_status_filter()
        return self

    @_copy_with
    def with_query_status_filter(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_query_status_filter()
        return self

    @_copy_with
    def with_filter(
        self,
        kind: Union[FilterKind, str],
        comparator: Union[ComparatorKind, str],
        value: Union[List[str], str],
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_filter(kind, comparator, value)
        return self

    @_copy_with
    def with_window_function(self, series_name: str, window_function: Union[WindowFunctionKind, str]) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_window_function(window_function)
        return self

    @_copy_with
    def with_group_by(self, series_name: str, group_by: Union[GroupByKind, str]) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by(group_by)
        return self

    @_copy_with
    def with_group_by_feature_status(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_feature_status()
        return self

    @_copy_with
    def with_group_by_feature_name(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_feature_name()
        return self

    @_copy_with
    def with_group_by_is_null(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_is_null()
        return self

    @_copy_with
    def with_group_by_resolver_status(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_resolver_status()
        return self

    @_copy_with
    def with_group_by_resolver_name(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_resolver_name()
        return self

    @_copy_with
    def with_group_by_query_status(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_query_status()
        return self

    @_copy_with
    def with_group_by_query_name(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_query_name()
        return self

    @_copy_with
    def with_group_by_resolver_type(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_resolver_type()
        return self

    @_copy_with
    def with_group_by_cache_hit(
        self,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_group_by_cache_hit()
        return self

    @_copy_with
    def with_time_shift(
        self,
        time_shift: int,
        series_name: str,
    ) -> "Chart":
        series_index, series = self._get_series_index(series_name=series_name)
        self._series[series_index] = series.with_time_shift(time_shift)
        return self

    @_copy_with
    def with_feature_link(self, feature: FeatureNameType) -> "Chart":
        self._entity_kind = ChartLinkKind.feature
        self._entity_id = str(feature) if isinstance(feature, FeatureWrapper) else feature
        return self

    @_copy_with
    def with_resolver_link(self, resolver: ResolverNameType) -> "Chart":
        self._entity_kind = ChartLinkKind.resolver
        self._entity_id = resolver.fqn if isinstance(resolver, Resolver) else resolver
        return self

    @_copy_with
    def with_query_link(self, query_name: str) -> "Chart":
        self._entity_kind = ChartLinkKind.query
        self._entity_id = query_name
        return self

    def keep(self) -> "Chart":
        self._keep = True
        return self

    def __str__(self) -> str:
        return f"Chart(name='{self._name}')"

    def __getitem__(self, key: str) -> Union[Series, Formula]:
        for series in self._series:
            if series._name == key:
                return series
        for formula in self._formulas:
            if formula._name == key:
                return formula
        raise ValueError(f"No series or formula named '{key}' exists in Chart {self._name}")

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def __hash__(self):
        name = self._name if self._name else "."

        window_period = self._window_period if self._window_period else "."
        chart_string = f"chart.{name}.{window_period}"

        series_hash = ".".join(sorted([str(hash(series)) for series in self._series]))
        formulas = ".".join(sorted([str(hash(formula)) for formula in self._formulas]))
        trigger = str(hash(self._trigger)) if self._trigger else "."

        return zlib.crc32(chart_string.encode() + series_hash.encode() + formulas.encode() + trigger.encode())
