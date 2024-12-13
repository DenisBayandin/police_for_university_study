from dataclasses import dataclass, fields
from abc import ABC, abstractmethod
from datetime import datetime

from app.utils.db_execute import list_db_execute, db_execute


@dataclass
class BaseDataClass(ABC):
    @classmethod
    def pk(cls):
        pk_attr = []
        for field in fields(cls):
            if field.metadata.get("primary_key") is True:
                pk_attr.append(field)
        return pk_attr

    @classmethod
    def table_fields(cls):
        return fields(cls)

    @classmethod
    def table_fields_names(cls):
        return [field.name for field in cls.table_fields()]

    @classmethod
    def table_name(cls):
        return "".join(cls.__name__.split("_")).lower()

    @classmethod
    @abstractmethod
    def create_db_table(cls):
        ...

    @classmethod
    @abstractmethod
    def drop_db_table(cls):
        ...

    @classmethod
    @list_db_execute()
    def list(cls):
        return f"""
        SELECT {",".join(cls.table_fields_names())} FROM public.{cls.table_name()};
        """

    @abstractmethod
    def retrieve(self):
        ...

    @abstractmethod
    def create(self):
        ...

    @classmethod
    @db_execute()
    def update(cls, pk_values: dict, **kwargs):
        if hasattr(cls, "updated_at"):
            kwargs["updated_at"] = datetime.now()
        if not pk_values:
            raise ValueError("Primary key values must be provided.")
        if not kwargs:
            raise ValueError("No fields provided for update.")
        pk_fields = {field.name for field in cls.pk()}
        invalid_pks = [key for key in pk_values if key not in pk_fields]
        if invalid_pks:
            raise ValueError(f"Invalid primary key fields: {', '.join(invalid_pks)}")
        valid_fields = {field.name for field in fields(cls)}
        invalid_fields = [key for key in kwargs if key not in valid_fields]
        if invalid_fields:
            raise ValueError(f"Invalid fields for update: {', '.join(invalid_fields)}")
        fields_to_update = [
            f'"{key}" = \'{value}\''
            for key, value in kwargs.items()
            if key not in pk_fields and value
        ]
        if not fields_to_update:
            raise ValueError("No valid fields to update.")
        pk_condition = " AND ".join(
            [f'"{key}" = \'{value}\'' for key, value in pk_values.items()]
        )
        return f"""
        UPDATE public.{cls.table_name()}
        SET {", ".join(fields_to_update)}
        WHERE {pk_condition};
        """

    @classmethod
    @db_execute()
    def delete(cls, **pk_values):
        if not pk_values:
            raise ValueError("Primary key values must be provided.")
        pk_fields = {field.name for field in cls.pk()}
        invalid_pks = [key for key in pk_values if key not in pk_fields]
        if invalid_pks:
            raise ValueError(f"Invalid primary key fields: {', '.join(invalid_pks)}")
        pk_condition = " AND ".join(
            [f'"{key}" = \'{value}\'' for key, value in pk_values.items()]
        )
        return f"""
        DELETE FROM public.{cls.table_name()}
        WHERE {pk_condition};
        """
