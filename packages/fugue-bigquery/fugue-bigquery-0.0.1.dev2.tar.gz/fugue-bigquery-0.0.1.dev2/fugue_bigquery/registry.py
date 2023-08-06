from typing import Any, Optional

from fugue import ExecutionEngine, is_pandas_or, SQLEngine
from fugue.plugins import (
    infer_execution_engine,
    parse_execution_engine,
    parse_sql_engine,
)
from triad import ParamDict

from ._utils import is_bq_ibis_table
from .client import BigQueryClient
from .dataframe import BigQueryDataFrame
from .execution_engine import BigQueryExecutionEngine, BigQuerySQLEngine


@parse_execution_engine.candidate(
    matcher=lambda engine, conf, **kwargs: isinstance(engine, str)
    and (engine == "bq" or engine == "bigquery"),
    priority=2.5,
)
def _parse_bq(engine: str, conf: Any, **kwargs) -> ExecutionEngine:
    _conf = ParamDict(conf)
    client = BigQueryClient.get_or_create(_conf)
    return BigQueryExecutionEngine(client, _conf)


@infer_execution_engine.candidate(
    lambda objs: is_pandas_or(objs, BigQueryDataFrame)
    or any(
        is_bq_ibis_table(x) or (isinstance(x, str) and x == "force_bq") for x in objs
    )
)
def _infer_bq_engine(objs: Any) -> Any:
    return "bq"


@parse_sql_engine.candidate(
    lambda engine, *args, **kwargs: isinstance(engine, str)
    and engine in ["bq", "bigquery"]
)
def _to_bq_sql_engine(
    engine: str,
    execution_engine: Optional[ExecutionEngine] = None,
    **kwargs: Any,
) -> SQLEngine:
    return BigQuerySQLEngine(execution_engine)
