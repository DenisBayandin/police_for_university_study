from dataclasses import dataclass, field
from datetime import datetime

from .base_data_class import BaseDataClass
from ..utils.db_execute import db_execute, list_db_execute


@dataclass
class Personnel(BaseDataClass):
    police_department: str = field(metadata={"primary_key": True})
    staff: str = field(metadata={"primary_key": True})
    present_post: str
    is_active: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    @db_execute()
    def create_db_table(cls):
        return f"""
            CREATE TABLE public.{cls.table_name()} (
              "police_department" VARCHAR(6) NOT NULL,
              "staff" VARCHAR(255) NOT NULL,
              "present_post" VARCHAR(255) NOT NULL,
              "is_active" BOOLEAN,
              "created_at" TIMESTAMP,
              "updated_at" TIMESTAMP,
              PRIMARY KEY ("police_department", "staff")
            );
            
            ALTER TABLE public.{cls.table_name()} ADD CONSTRAINT "fk_personnel__police_department" FOREIGN KEY ("police_department") REFERENCES public."policedepartment" ("ovd_code") ON DELETE CASCADE;
            
            ALTER TABLE public.{cls.table_name()} ADD CONSTRAINT "fk_personnel__staff" FOREIGN KEY ("staff") REFERENCES public."staff" ("personal_number") ON DELETE CASCADE;
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
