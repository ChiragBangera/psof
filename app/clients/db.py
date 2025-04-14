from typing import Optional
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select


class DatabaseClient:
    def __init__(self, config, tables: Optional[list[str]]) -> None:
        self.config = config
        self.engine = create_engine(self.config.host, future=True)
        self.session = Session(bind=self.engine, future=True)
        self.metadata = MetaData()
        self._reflect_method()

        if tables:  # does not trigger if tables is None or len(tables) == 0
            self._set_internal_database_tables(tables)

    def _reflect_method(self) -> None:
        self.metadata.reflect(
            bind=self.engine
        )  # getting tables fails if tables don't have primary key

    def _set_internal_database_tables(self, tables: list[str]):
        for table in tables:
            setattr(self, table, self.metadata.tables[table])

    def get_first(self, query: Select) -> Optional[dict]:
        with self.session.begin():
            res = self.session.execute(query).mappings().first()
        return res

    def get_all(self, query: Select) -> list[dict]:
        with self.session.begin():
            res = self.session.execute(query).mappings().all()
        return res

    def get_paginated(self, query: Select, limit: int, offset: int) -> list[dict]:
        query = query.limit(limit).offset(offset)
        return self.get_all(query)
