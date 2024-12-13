from dataclasses import dataclass, field

from .base_data_class import BaseDataClass
from datetime import datetime
from ..utils.db_execute import db_execute, list_db_execute


@dataclass
class Assignment(BaseDataClass):
    personnel_police_department: str = field(metadata={"primary_key": True})
    personnel_staff: str = field(metadata={"primary_key": True})
    technic_department_police_department: str = field(metadata={"primary_key": True})
    technic_department_technic_maker: str = field(metadata={"primary_key": True})
    technic_department_technic_serial_number: str = field(metadata={"primary_key": True})
    is_active: bool
    created_at = datetime.now()
    updated_at = datetime.now()

    @classmethod
    @db_execute()
    def create_db_table(cls):
        return f"""
            CREATE TABLE public.{cls.table_name()} (
              "personnel_police_department" VARCHAR(6) NOT NULL,
              "personnel_staff" VARCHAR(255) NOT NULL,
              "technic_department_police_department" VARCHAR(6) NOT NULL,
              "technic_department_technic_maker" VARCHAR(255) NOT NULL,
              "technic_department_technic_serial_number" VARCHAR(12) NOT NULL,
              "is_active" BOOLEAN,
              "created_at" TIMESTAMP,
              "updated_at" TIMESTAMP,
              PRIMARY KEY ("personnel_police_department", "personnel_staff", "technic_department_police_department", "technic_department_technic_maker", "technic_department_technic_serial_number")
            );
            
            ALTER TABLE public.{cls.table_name()} ADD CONSTRAINT "fk_assignment__personnel_police_department__personnel_staff" FOREIGN KEY ("personnel_police_department", "personnel_staff") REFERENCES public."personnel" ("police_department", "staff") ON DELETE CASCADE;
            
            ALTER TABLE public.{cls.table_name()} ADD CONSTRAINT "fk_assignment__technic_department_police_department__technic_de" FOREIGN KEY ("technic_department_police_department", "technic_department_technic_maker", "technic_department_technic_serial_number") REFERENCES public."technicdepartment" ("police_department", "technic_maker", "technic_serial_number") ON DELETE CASCADE;
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

