import logging
import urllib

from sqlalchemy import pool
from sqlalchemy import types
from sqlalchemy import types as sqltypes
from sqlalchemy import util
from sqlalchemy.engine import default, reflection
from sqlalchemy.sql import compiler, elements
from sqlalchemy.types import BIGINT, BINARY, BOOLEAN, CHAR, DATE, FLOAT, INTEGER, SMALLINT, TIME, TIMESTAMP, VARCHAR

import pyocient

try:
    from version import __version__

    version = __version__
except ImportError:
    version = "1.0.0"

logger = logging.getLogger("sqlalchemy_ocient")


class OcientType(types.TypeEngine):
    pass


class IP(OcientType):
    __visit_name__ = "IP"


class IPV4(OcientType):
    __visit_name__ = "IPV4"


class HASH(OcientType):
    __visit_name__ = "HASH"


class DECIMAL(OcientType):
    __visit_name__ = "DECIMAL"


class DOUBLE(OcientType):
    __visit_name__ = "DOUBLE"


class POINT(OcientType):
    __visit_name__ = "POINT"


class LINESTRING(OcientType):
    __visit_name__ = "LINESTRING"


class POLYGON(OcientType):
    __visit_name__ = "POLYGON"


class BYTE(OcientType):
    __visit_name__ = "BYTE"


class UUID(OcientType):
    __visit_name__ = "UUID"


class ARRAY(OcientType):
    __visit_name__ = "ARRAY"


class TUPLE(OcientType):
    __visit_name__ = "TUPLE"


class OcientExecutionContext(default.DefaultExecutionContext):
    pass


class OcientCompiler(compiler.SQLCompiler):
    extract_map = compiler.SQLCompiler.extract_map.copy()
    extract_map.update(
        {
            "month": "m",
            "day": "d",
            "year": "yyyy",
            "second": "s",
            "hour": "h",
            "doy": "y",
            "minute": "n",
            "quarter": "q",
            "dow": "w",
            "week": "ww",
        }
    )

    def visit_binary(self, binary, override_operator=None, eager_grouping=False, **kw):
        return super(OcientCompiler, self).visit_binary(
            binary,
            override_operator=override_operator,
            eager_grouping=eager_grouping,
            **kw,
        )

    def for_update_clause(self, select):
        """FOR UPDATE is not supported by Ocient; silently ignore"""
        return ""

    def visit_column(self, column, add_to_result_map=None, include_table=True, **kwargs):
        name = orig_name = column.name
        if name is None:
            name = self._fallback_column_name(column)

        is_literal = column.is_literal
        if not is_literal and isinstance(name, elements._truncated_label):
            name = self._truncated_identifier("colident", name)

        if add_to_result_map is not None:
            add_to_result_map(name, orig_name, (column, name, column.key), column.type)

        if is_literal:
            name = self.escape_literal_column(name)
        else:
            name = self.preparer.quote(name)
        table = column.table
        if table is None or not include_table or not table.named_with_column:
            return name
        else:
            effective_schema = self.preparer.schema_for_object(table)
            schema_prefix = ""
            tablename = table.name
            if isinstance(tablename, elements._truncated_label):
                tablename = self._truncated_identifier("alias", tablename)

            return schema_prefix + self.preparer.quote(tablename) + "." + name

    def order_by_clause(self, select, **kw):
        order_by = select._order_by_clause
        if len(str(order_by)) > 0:
            order_by_str = str(order_by)
            order_by_str = order_by_str.replace(".", "_")
            if order_by_str.lower() == "count(*)":
                if "(" in order_by_str:
                    if "DESC" in order_by_str:
                        k = order_by_str.rfind(" DESC")
                        part1 = order_by_str[:k]
                        part1 = part1.upper()
                        part1 = '"' + part1 + '"'
                        order_by_str = '"' + part1 + '"' + order_by_str[k:]
                    elif "ASC" in order_by_str:
                        k = order_by_str.rfind(" ASC")
                        part1 = order_by_str[:k]
                        part1 = '"' + part1 + '"'
                        part1 = part1.upper()
                        order_by_str = '"' + part1 + '"' + order_by_str[k:]
                    else:
                        order_by_str = '"' + order_by_str + '"'
            return " ORDER BY " + order_by_str
        else:
            return ""

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += " \n LIMIT " + self.process(select._limit_clause, **kw)
            if "param_1" in self.params:
                text = text.replace("%(param_1)s", f"{self.params['param_1']}")
        return text

    def visit_join(self, join, asfrom=False, **kwargs):
        return (
            "("
            + self.process(join.left, asfrom=True)
            + (join.isouter and " LEFT OUTER JOIN " or " INNER JOIN ")
            + self.process(join.right, asfrom=True)
            + " ON "
            + self.process(join.onclause)
            + ")"
        )

    def visit_extract(self, extract, **kw):
        field = self.extract_map.get(extract.field, extract.field)
        return 'DATEPART("%s", %s)' % (field, self.process(extract.expr, **kw))


class OcientTypeCompiler(compiler.GenericTypeCompiler):
    def visit_BOOLEAN(self, type_, **kw):
        return "BOOLEAN"

    def visit_INT(self, type_, **kw):
        return "INT"

    def visit_INT8(self, type_, **kw):
        return "INT8"

    def visit_UINT8(self, type_, **kw):
        return "UINT8"

    def visit_INT16(self, type_, **kw):
        return "INT16"

    def visit_UINT16(self, type_, **kw):
        return "UINT16"

    def visit_INT32(self, type_, **kw):
        return "INT32"

    def visit_UINT32(self, type_, **kw):
        return "UINT32"

    def visit_INT64(self, type_, **kw):
        return "INT64"

    def visit_SHORT(self, type_, **kw):
        return "SHORT"

    def visit_LONG(self, type_, **kw):
        return "LONG"

    def visit_FLOAT(self, type_, **kw):
        return "FLOAT"

    def visit_DOUBLE(self, type_, **kw):
        return "DOUBLE"

    def visit_UINT64(self, type_, **kw):
        return "UINT64"

    def visit_FLOAT32(self, type_, **kw):
        return "FLOAT32"

    def visit_FLOAT64(self, type_, **kw):
        return "FLOAT64"

    def visit_BLOB(self, type_, **kw):
        return "BLOB"

    def visit_IPV4(self, type_, **kw):
        return "IPV4"

    def visit_UUID(self, type_, **kw):
        return "UUID"

    def visit_NUMERICXY(self, type_, **kw):
        return "NUMERICXY"

    def visit_HASH(self, type_, **kw):
        return "HASH"


ischema_names = {
    "BIGINT": BIGINT,
    "LONG": BIGINT,
    "BINARY": BINARY,
    "HASH": HASH,
    "BOOLEAN": BOOLEAN,
    "CHARACTER": CHAR,
    "CHAR": CHAR,
    "DATE": DATE,
    "DECIMAL": DECIMAL,
    "DOUBLE PRECISION": DOUBLE,
    "DOUBLE": DOUBLE,
    "INT": INTEGER,
    "IPV4": IPV4,
    "IP": IP,
    "POINT": POINT,
    "ST_POINT": POINT,
    "LINESTRING": LINESTRING,
    "ST_LINESTRING": LINESTRING,
    "POLYGON": POLYGON,
    "ST_POLYGON": POLYGON,
    "REAL": FLOAT,
    "FLOAT": FLOAT,
    "SINGLE PRECISION": FLOAT,
    "SMALLINT": SMALLINT,
    "SHORT": SMALLINT,
    "TIME": TIME,
    "TIMESTAMP": TIMESTAMP,
    "TINYINT": BYTE,
    "BYTE": BYTE,
    "UUID": UUID,
}

mutable_types = {
    "ARRAY": ARRAY,
    "TUPLE": TUPLE,
    "HASH": HASH,
    "ST_POINT": POINT,
}


class OcientIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = compiler.RESERVED_WORDS.copy()
    reserved_words.update(["value", "text"])

    def __init__(self, dialect):
        super(OcientIdentifierPreparer, self).__init__(dialect, initial_quote='"', final_quote='"')


class OcientDialect(default.DefaultDialect):
    name = "ocient"
    driver = "ocient"
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_unicode_statements = False
    supports_unicode_binds = False
    supports_simple_order_by_label = True

    poolclass = pool.SingletonThreadPool
    type_compiler = OcientTypeCompiler
    statement_compiler = OcientCompiler
    preparer = OcientIdentifierPreparer
    execution_ctx_cls = OcientExecutionContext

    ischema_names = ischema_names

    @classmethod
    def dbapi(cls):
        return pyocient

    def do_execute(self, cursor, statement, parameters, context=None):
        statement = statement.decode()
        parameters = {key.decode(): val for key, val in parameters.items()}
        if not parameters:
            parameters = None
        cursor.execute(statement, parameters)

    def create_connect_args(self, url):
        urlstr = urllib.parse.unquote(str(url)).replace("ocientdb", "ocient")
        return [[urlstr], {}]

    """
    @reflection.cache
    def get_schema_names(self, connection, **kw):
        s = "GET SCHEMA"
        cursor = connection.execute(s)
        schemas = [row[0] for row in cursor]
        schemas.append("public")
        return schemas
    """

    @reflection.cache
    def get_schema_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            schema_names = []
            for rows in cursor.tables(schema="%", table="%"):
                rows = [str(r) for r in rows]
                if rows[1] not in schema_names:
                    schema_names.append(rows[1])
            schema_names.append("public")
            cursor.close()
        finally:
            conn.close()
        return schema_names

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            table_names = []
            if schema == None:
                sc = "%"
            else:
                sc = schema
            for rows in cursor.tables(schema=sc, table="%"):
                rows = [str(r) for r in rows]
                table_names.append(rows[2])
            cursor.close()
        finally:
            conn.close()
        return table_names

    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            view_names = []
            if schema == None:
                sc = "%"
            else:
                sc = schema
            for rows in cursor.views():
                rows = [str(r) for r in rows]
                view_names.append(rows[2])
            cursor.close()
        finally:
            conn.close()
        return view_names

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        conn = connection.engine.raw_connection()
        try:
            cursor = conn.cursor()
            query = f"select 1 FROM {schema}.{table_name} limit 1"
            cursor.execute(query)
            columns = []
            for rows in cursor.columns(schema=schema, table=table_name, column="%"):
                col_info = self._get_column_info(rows[3], rows[5], rows[10], rows[11], rows[15])
                columns.append(col_info)
            cursor.close()
        finally:
            conn.close()
        return columns

    def has_table(self, connection, table_name, schema=None):
        conn = connection.engine.raw_connection()
        cursor = conn.cursor()
        query = f"SELECT 1 AS has_table FROM {schema}.{table_name}"
        try:
            c = cursor.execute(query)
            columns = [col[3] for col in c.columns(table=table_name, schema=schema)]
        except pyocient.Error:
            return False
        else:
            return True

    def _get_column_info(self, name, type_, nullable, remarks, length):

        for mutable_type in mutable_types:
            if type_.startswith(mutable_type):
                coltype = mutable_types[mutable_type]
                break
        else:
            coltype = self.ischema_names.get(type_, None)

        kwargs = {}

        if coltype in (CHAR, VARCHAR):
            args = (length,)
        else:
            args = ()

        if coltype:
            coltype = coltype(*args, **kwargs)
        else:
            util.warn("Did not recognize type '%s' of column '%s'" % (type_, name))
            coltype = sqltypes.NULLTYPE

        column_info = dict(name=name, type=coltype, nullable=nullable, remarks=remarks)
        return column_info

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        constrained_columns = []
        cdict = {"constrained_columns": constrained_columns, "name": None}
        return cdict

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):

        foreign_keys = []
        return foreign_keys

    @reflection.cache
    def get_unique_constraints(self, connection, table_name, schema=None, **kw):

        constraints = []
        return constraints

    @reflection.cache
    def get_check_constraints(self, connection, table_name, schema=None, **kw):

        constraints = []
        return constraints

    @reflection.cache
    def get_table_comment(self, connection, table_name, schema=None, **kw):

        comment = {"text": None}
        return comment

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        # TODO Leverage info schema to redurn indexes. See https://ocient.atlassian.net/browse/DB-23236
        indexes = []
        return indexes

    def _check_unicode_returns(self, connection, additional_tests=None):
        return False

    def _check_unicode_description(self, connection):
        return False

    def do_rollback(self, dbapi_connection):
        # No support for transactions.
        pass


dialect = OcientDialect
