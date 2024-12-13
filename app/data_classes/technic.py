from dataclasses import dataclass, field

from .base_data_class import BaseDataClass
from ..utils.db_execute import db_execute, list_db_execute


@dataclass
class Technic(BaseDataClass):
    maker: str = field(metadata={"primary_key": True})
    serial_number: str = field(metadata={"primary_key": True})
    type: str
    name: str
    registration_number: str

    @classmethod
    @db_execute()
    def create_db_table(cls):
        return f"""
            CREATE TABLE public.{cls.table_name()} (
              "maker" VARCHAR(255) NOT NULL,
              "serial_number" VARCHAR(12) NOT NULL,
              "type" VARCHAR(255) NOT NULL,
              "name" VARCHAR(255) NOT NULL,
              "registration_number" VARCHAR(12) NOT NULL,
              PRIMARY KEY ("maker", "serial_number")
            );
        """

    @classmethod
    @db_execute()
    def drop_db_table(cls):
        return f"""DROP TABLE IF EXISTS public.{cls.table_name()} CASCADE;"""

    @db_execute()
    def create(self):
        values = [getattr(self, field_name) for field_name in self.table_fields_names()]
        return f"""
        INSERT INTO public."{self.table_name()}" ({", ".join(self.table_fields_names())})
        VALUES ({", ".join(f"'{value}'" for value in values)});
        """

    @classmethod
    @list_db_execute()
    def retrieve(cls, **kwargs):
        pk_data = {pk_field.name: kwargs.get(pk_field.name) for pk_field in cls.pk()}
        return f"SELECT {",".join(cls.table_fields_names())} FROM public.{cls.table_name()} WHERE {" AND ".join(
            [f'"{key}" = \'{value}\'' for key, value in pk_data.items()]
        )}"
