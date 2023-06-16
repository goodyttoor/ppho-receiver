import datetime
from typing import List, Annotated

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class ReceiveData(BaseModel):
    table_name: str
    data: List[dict]


class Person(SQLModel, table=True):
    __tablename__ = "person"

    hcode: Annotated[str, Field(max_length=9, primary_key=True)]
    cid: Annotated[str, Field(max_length=13, primary_key=True)]
    PRENAME: Annotated[str | None, Field(max_length=5)] = None
    fname: Annotated[str | None, Field(max_length=100)] = None
    lname: Annotated[str | None, Field(max_length=100)] = None
    birth_date: datetime.date | None = None
    sex: Annotated[str | None, Field(max_length=1)] = None
    race: Annotated[str | None, Field(max_length=3)] = None
    nation: Annotated[str | None, Field(max_length=3)] = None
    houseno: Annotated[str | None, Field(max_length=50)] = None
    moo: Annotated[str | None, Field(max_length=50)] = None
    ampur: Annotated[str | None, Field(max_length=20)] = None
    tambon: Annotated[str | None, Field(max_length=20)] = None
    province: Annotated[str | None, Field(max_length=20)] = None
    discharge: int | None = None
    d_update: datetime.datetime | None = None