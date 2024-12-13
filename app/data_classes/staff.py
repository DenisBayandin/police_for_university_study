from dataclasses import dataclass, field, fields

from .base_data_class import BaseDataClass
from ..utils.db_execute import db_execute, list_db_execute


@dataclass
class Staff(BaseDataClass):
    personal_number: str = field(metadata={"primary_key": True})
    full_name: str
    rank: str

    @classmethod
    def pk(cls):
        pk_attr = []
        for field in fields(cls):
            if field.metadata.get("primary_key") is True:
                pk_attr.append(field)
        return pk_attr


    @classmethod
    @db_execute()
    def create_db_table(cls):
        return f"""
        CREATE TABLE public.{cls.table_name()} (
          "personal_number" VARCHAR(255) PRIMARY KEY,
          "full_name" VARCHAR(255) NOT NULL,
          "rank" VARCHAR(255) NOT NULL
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
