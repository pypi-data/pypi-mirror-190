import logging
from typing import Generator, Optional

import sqlalchemy as sa
from datayoga_core import utils
from datayoga_core.blocks.relational import utils as relational_utils
from datayoga_core.context import Context
from datayoga_core.producer import Message
from datayoga_core.producer import Producer as DyProducer

logger = logging.getLogger("dy")


class Block(DyProducer):

    def init(self, context: Optional[Context] = None):
        engine, db_type = relational_utils.get_engine(self.properties.get("connection"), context)
        self.db_type = db_type

        self.schema = self.properties.get("schema")
        self.table = self.properties.get("table")
        self.opcode_field = self.properties.get("opcode_field")
        self.load_strategy = self.properties.get("load_strategy")
        self.keys = self.properties.get("keys")
        self.mapping = self.properties.get("mapping")

        self.tbl = sa.Table(self.table, sa.MetaData(schema=self.schema), autoload_with=engine)

        logger.debug(f"Connecting to {self.db_type}")
        self.connection = engine.connect()

    def produce(self) -> Generator[Message, None, None]:
        result = self.connection.execution_options(stream_results=True).execute(
            self.tbl.select()
        )

        while True:
            chunk = result.fetchmany(10000)
            if not chunk:
                break
            for row in chunk:
                yield utils.add_uid(dict(row))
