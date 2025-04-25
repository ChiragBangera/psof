from typing import Optional, Sequence, Union
from sqlalchemy import create_engine, MetaData, RowMapping
from sqlalchemy.sql.expression import Select, Delete, Insert
from databases import Database
import os


class DatabaseClient:
    def __init__(self, config, tables: Optional[list[str]]) -> None:
        self.config = config
        self.engine = create_engine(self.config.host, future=True)
        self.metadata = MetaData()
        self._reflect_method()

        if tables:  # does not trigger if tables is None or len(tables) == 0
            self._set_internal_database_tables(tables)

        if os.getenv("app_env") == "test":
            self.database = Database(self.config.host, force_rollback=True)
        else:
            self.database = Database(self.config.host)

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()

    def _reflect_method(self) -> None:
        self.metadata.reflect(
            bind=self.engine
        )  # getting tables fails if tables don't have primary key

    def _set_internal_database_tables(self, tables: list[str]):
        for table in tables:
            setattr(self, table, self.metadata.tables[table])

    async def get_first(self, query: Union[Select, Insert]) -> Optional[dict]:
        async with self.database.transaction():
            res = await self.database.fetch_one(query=query)
        return res

    async def get_all(self, query: Select) -> Sequence[RowMapping]:
        async with self.database.transaction():
            res = await self.database.fetch_all(query=query)
        return res

    async def get_paginated(
        self, query: Select, limit: int, offset: int
    ) -> Sequence[RowMapping]:
        query = query.limit(limit).offset(offset)
        return await self.get_all(query)

    async def execute_in_transaction(self, query: Delete):
        async with self.database.transaction():
            await self.database.execute(query)
