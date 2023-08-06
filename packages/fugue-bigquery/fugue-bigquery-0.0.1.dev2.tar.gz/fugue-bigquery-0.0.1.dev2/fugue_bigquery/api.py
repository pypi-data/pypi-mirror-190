from typing import Any, List, Optional

import fugue.api as fa
from fugue import AnyDataFrame, AnyExecutionEngine
from triad import Schema
from triad.utils.schema import quote_name

from ._utils import table_to_query
from .client import BigQueryClient
from .dataframe import BigQueryDataFrame
from .execution_engine import BigQueryExecutionEngine


def get_schema(query_or_table: str) -> Schema:
    query = (
        query_or_table
        if query_or_table.lower().startswith("select ")
        else f"SELECT * FROM {quote_name(query_or_table)}"
    )
    client = BigQueryClient.get_or_create(fa.get_current_conf())
    tdf = BigQueryDataFrame(client.ibis.sql(query))
    return tdf.schema


def load_table(
    table: str,
    columns: Optional[List[str]] = None,
    row_filter: Optional[str] = None,
    sample: float = 1.0,
    engine: AnyExecutionEngine = None,
    engine_conf: Any = None,
    as_fugue: bool = False,
    parallelism: Optional[int] = None,
    **read_kwargs: Any,
) -> AnyDataFrame:
    if sample < 1.0:
        return load_sql(
            table_to_query(
                table, columns=columns, row_filter=row_filter, sample=sample
            ),
            engine=engine,
            engine_conf=engine_conf,
            as_fugue=as_fugue,
            parallelism=parallelism,
            **read_kwargs,
        )
    with fa.engine_context(engine, engine_conf=engine_conf, infer_by=["force_bq"]) as e:
        if isinstance(e, BigQueryExecutionEngine) and row_filter is None:
            tb = e.client.table_to_ibis(table, columns)
            return e.to_df(tb) if as_fugue else tb
        else:
            client = BigQueryClient.get_or_create(fa.get_current_conf())
            if parallelism is None:
                parallelism = e.get_current_parallelism() * 2
            res = client.read_table(
                e,
                table,
                columns=columns,
                row_filter=row_filter,
                max_stream_count=parallelism,
                **read_kwargs,
            )
            return res if as_fugue else fa.get_native_as_df(res)


def load_sql(
    query: str,
    engine: AnyExecutionEngine = None,
    engine_conf: Any = None,
    as_fugue: bool = False,
    parallelism: Optional[int] = None,
    **read_kwargs: Any,
) -> AnyDataFrame:
    with fa.engine_context(engine, engine_conf=engine_conf) as e:
        if isinstance(e, BigQueryExecutionEngine):
            res: Any = e._raw_select(query, {})
            return BigQueryDataFrame(res) if as_fugue else res
        else:
            client = BigQueryClient.get_or_create(fa.get_current_conf())
            tb = client.query_to_table(query, is_view=False)
            if parallelism is None:
                parallelism = e.get_current_parallelism() * 2
            res = client.read_table(
                e,
                tb,
                max_stream_count=parallelism,
                **read_kwargs,
            )
            return res if as_fugue else fa.get_native_as_df(res)
