import datetime
from typing import List, Optional

from pydantic import BaseModel, condecimal
from sqlmodel import Field, SQLModel


# Base model for data receiver
class ReceiveData(BaseModel):
    table_name: str
    data: List[dict]


# Model for admission table
class Admission(SQLModel, table=True):
    __tablename__ = 'admission'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    AN: str = Field(max_length=9, primary_key=True)
    DATETIME_ADMIT: datetime.datetime = Field(primary_key=True)
    WARDADMIT: str = Field(max_length=5)
    INSTYPE: str = Field(max_length=4)
    TYPEIN: str = Field(max_length=1)
    REFERINHOSP: Optional[str] = Field(default=None, max_length=5)
    CAUSEIN: Optional[str] = Field(default=None, max_length=1)
    ADMITWEIGHT: Optional[condecimal(max_digits=5, decimal_places=1)] = Field(default=None)
    ADMITHEIGHT: Optional[condecimal(max_digits=3)] = Field(default=None)
    DATETIME_DISCH: datetime.datetime = Field(primary_key=True)
    WARDDISCH: str = Field(max_length=5)
    DISCHSTATUS: str = Field(max_length=1)
    DISCHTYPE: str = Field(max_length=1)
    REFEROUTHOSP: Optional[str] = Field(default=None, max_length=5)
    CAUSEOUT: Optional[str] = Field(default=None, max_length=1)
    COST: Optional[condecimal(max_digits=11, decimal_places=2)] = Field(default=None)
    PRICE: condecimal(max_digits=11, decimal_places=2)
    PAYPRICE: condecimal(max_digits=11, decimal_places=2)
    ACTUALPAY: condecimal(max_digits=11, decimal_places=2)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    DRG: Optional[str] = Field(default='0', max_length=5)
    RW: Optional[condecimal(max_digits=11, decimal_places=4)] = Field(default=0.000)
    ADJRW: Optional[condecimal(max_digits=11, decimal_places=4)] = Field(default=0.000)
    ERROR: Optional[str] = Field(default='0', max_length=2)
    WARNING: Optional[str] = Field(default='0', max_length=4)
    ACTLOS: Optional[condecimal(max_digits=4)] = Field(default=0)
    GROUPER_VERSION: Optional[str] = Field(default='0', max_length=20)
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class CommunityService(SQLModel, table=True):
    __tablename__ = 'community_service'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    COMSERVICE: str = Field(max_length=7, primary_key=True)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class Dental(SQLModel, table=True):
    __tablename__ = 'dental'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    DENTTYPE: str = Field(max_length=1)
    SERVPLACE: str = Field(max_length=1)
    PTEETH: Optional[condecimal(max_digits=2)] = Field(default=None)
    PCARIES: Optional[condecimal(max_digits=2)] = Field(default=None)
    PFILLING: Optional[condecimal(max_digits=2)] = Field(default=None)
    PEXTRACT: Optional[condecimal(max_digits=2)] = Field(default=None)
    DTEETH: Optional[condecimal(max_digits=2)] = Field(default=None)
    DCARIES: Optional[condecimal(max_digits=2)] = Field(default=None)
    DFILLING: Optional[condecimal(max_digits=2)] = Field(default=None)
    DEXTRACT: Optional[condecimal(max_digits=2)] = Field(default=None)
    NEED_FLUORIDE: Optional[str] = Field(default=None, max_length=1)
    NEED_SCALING: Optional[str] = Field(default=None, max_length=1)
    NEED_SEALANT: Optional[condecimal(max_digits=2)] = Field(default=None)
    NEED_PFILLING: Optional[condecimal(max_digits=2)] = Field(default=None)
    NEED_DFILLING: Optional[condecimal(max_digits=2)] = Field(default=None)
    NEED_PEXTRACT: Optional[condecimal(max_digits=2)] = Field(default=None)
    NEED_DEXTRACT: Optional[condecimal(max_digits=2)] = Field(default=None)
    NPROSTHESIS: Optional[str] = Field(default=None, max_length=1)
    PERMANENT_PERMANENT: Optional[condecimal(max_digits=6)] = Field(default=None)
    PERMANENT_PROSTHESIS: Optional[condecimal(max_digits=6)] = Field(default=None)
    PROSTHESIS_PROSTHESIS: Optional[condecimal(max_digits=6)] = Field(default=None)
    GUM: Optional[str] = Field(default=None, max_length=6)
    SCHOOLTYPE: Optional[str] = Field(default=None, max_length=1)
    CLASS: Optional[str] = Field(default=None, max_length=1)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class DiagnosisIpd(SQLModel, table=True):
    __tablename__ = 'diagnosis_ipd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    AN: str = Field(max_length=9, primary_key=True)
    DATETIME_ADMIT: datetime.datetime = Field(primary_key=True)
    WARDDIAG: str = Field(max_length=5, primary_key=True)
    DIAGTYPE: str = Field(max_length=1, primary_key=True)
    DIAGCODE: str = Field(max_length=6, primary_key=True)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class DiagnosisOpd(SQLModel, table=True):
    __tablename__ = 'diagnosis_opd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    DIAGTYPE: str = Field(max_length=1, primary_key=True)
    DIAGCODE: str = Field(max_length=6, primary_key=True)
    CLINIC: str = Field(max_length=5, primary_key=True)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class OcScfcIpd(SQLModel, table=True):
    __tablename__ = 'oc_scfc_ipd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    AN: str = Field(max_length=9, primary_key=True)
    DATETIME_ADMIT: datetime.datetime = Field(primary_key=True)
    WARDDIAG: str = Field(max_length=5, primary_key=True)
    DIAGTYPE: str = Field(max_length=1, primary_key=True)
    DIAGCODE: str = Field(max_length=6, primary_key=True)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class OcScfcOpd(SQLModel, table=True):
    __tablename__ = 'oc_scfc_opd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    DIAGTYPE: str = Field(max_length=1, primary_key=True)
    DIAGCODE: str = Field(max_length=6, primary_key=True)
    CLINIC: str = Field(max_length=5, primary_key=True)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class PersonCid(SQLModel, table=True):
    __tablename__ = 'person_cid'

    person_id: Optional[str] = Field(default=None, max_length=13, primary_key=True)


class PersonDb(SQLModel, table=True):
    __tablename__ = 'person_db'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    CID: Optional[str] = Field(default=None, max_length=13)
    PID: str = Field(max_length=15, primary_key=True)
    HID: Optional[str] = Field(default=None, max_length=14)
    PRENAME: str = Field(default='', max_length=3)
    NAME: str = Field(default='', max_length=50)
    LNAME: str = Field(default='', max_length=50)
    HN: Optional[str] = Field(default=None, max_length=15)
    SEX: str = Field(default='', max_length=1)
    BIRTH: datetime.date = Field(default='0000-00-00')
    MSTATUS: Optional[str] = Field(default=None, max_length=1)
    OCCUPATION_OLD: Optional[str] = Field(default=None, max_length=3)
    OCCUPATION_NEW: Optional[str] = Field(default=None, max_length=4)
    RACE: Optional[str] = Field(default=None, max_length=3)
    NATION: str = Field(default='', max_length=3)
    RELIGION: Optional[str] = Field(default=None, max_length=2)
    EDUCATION: Optional[str] = Field(default=None, max_length=2)
    FSTATUS: Optional[str] = Field(default=None, max_length=1)
    FATHER: Optional[str] = Field(default=None, max_length=13)
    MOTHER: Optional[str] = Field(default=None, max_length=13)
    COUPLE: Optional[str] = Field(default=None, max_length=13)
    VSTATUS: Optional[str] = Field(default=None, max_length=1)
    MOVEIN: Optional[datetime.date] = Field(default=None)
    DISCHARGE: Optional[str] = Field(default=None, max_length=1)
    DDISCHARGE: Optional[datetime.date] = Field(default=None)
    ABOGROUP: Optional[str] = Field(default=None, max_length=1)
    RHGROUP: Optional[str] = Field(default=None, max_length=1)
    LABOR: Optional[str] = Field(default=None, max_length=2)
    PASSPORT: Optional[str] = Field(default=None, max_length=8)
    TYPEAREA: str = Field(default='', max_length=1)
    D_UPDATE: datetime.datetime = Field(default='0000-00-00 00:00:00')
    check_hosp: str = Field(default='', max_length=5)
    check_typearea: str = Field(default='', max_length=1)
    addr: Optional[str] = Field(default=None, max_length=100)
    vhid: Optional[str] = Field(default=None, max_length=8)
    check_vhid: Optional[str] = Field(default=None, max_length=8)
    maininscl: Optional[str] = Field(default=None, max_length=5)
    inscl: Optional[str] = Field(default=None, max_length=5)
    error_code: Optional[str] = Field(default=None, max_length=255)
    home: Optional[condecimal(max_digits=1)] = Field(default=0)
    TELEPHONE: Optional[str] = Field(default=None, max_length=15)
    MOBILE: Optional[str] = Field(default=None, max_length=15)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)
    person_id: Optional[str] = Field(default=None, max_length=13)


class ProcedureIpd(SQLModel, table=True):
    __tablename__ = 'procedure_ipd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    AN: str = Field(max_length=9, primary_key=True)
    DATETIME_ADMIT: datetime.datetime = Field(primary_key=True)
    WARDSTAY: str = Field(max_length=5, primary_key=True)
    PROCEDCODE: str = Field(max_length=7, primary_key=True)
    TIMESTART: datetime.datetime = Field(default=None, primary_key=True)
    TIMEFINISH: Optional[datetime.datetime] = Field(default=None)
    SERVICEPRICE: Optional[condecimal(max_digits=11, decimal_places=2)]
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class ProcedureOpd(SQLModel, table=True):
    __tablename__ = 'procedure_opd'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    CLINIC: str = Field(max_length=5, primary_key=True)
    PROCEDCODE: str = Field(max_length=7, primary_key=True)
    SERVICEPRICE: Optional[condecimal(max_digits=11, decimal_places=2)]
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class Rehabilitation(SQLModel, table=True):
    __tablename__ = 'rehabilitation'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: Optional[str] = Field(default=None, max_length=16)
    AN: Optional[str] = Field(default=None, max_length=9)
    DATE_ADMIT: Optional[datetime.datetime] = Field(default=None)
    DATE_SERV: datetime.date = Field(primary_key=True)
    DATE_START: Optional[datetime.date] = Field(default=None)
    DATE_FINISH: Optional[datetime.date] = Field(default=None)
    REHABCODE: str = Field(max_length=7, primary_key=True)
    AT_DEVICE: Optional[str] = Field(default=None, max_length=10)
    AT_NO: Optional[condecimal(max_digits=2)] = Field(default=None)
    REHABPLACE: Optional[str] = Field(default=None, max_length=5)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class Service(SQLModel, table=True):
    __tablename__ = 'service'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    HN: Optional[str] = Field(default=None, max_length=15)
    SEQ: str = Field(max_length=16, primary_key=True)
    DATE_SERV: datetime.date = Field(primary_key=True)
    TIME_SERV: Optional[str] = Field(default=None, max_length=6)
    LOCATION: Optional[str] = Field(default=None, max_length=1)
    INTIME: Optional[str] = Field(default=None, max_length=1)
    INSTYPE: str = Field(max_length=4, primary_key=True)
    INSID: Optional[str] = Field(default=None, max_length=18)
    MAIN: Optional[str] = Field(default=None, max_length=5)
    TYPEIN: str = Field(max_length=1, primary_key=True)
    REFERINHOSP: Optional[str] = Field(default=None, max_length=5)
    CAUSEIN: Optional[str] = Field(default=None, max_length=1)
    CHIEFCOMP: Optional[str] = Field(default=None, max_length=255)
    SERVPLACE: str = Field(max_length=1, primary_key=True)
    BTEMP: Optional[condecimal(max_digits=4, decimal_places=1)] = Field(default=None)
    SBP: Optional[condecimal(max_digits=3)] = Field(default=None)
    DBP: Optional[condecimal(max_digits=3)] = Field(default=None)
    PR: Optional[condecimal(max_digits=3)] = Field(default=None)
    RR: Optional[condecimal(max_digits=3)] = Field(default=None)
    TYPEOUT: str = Field(max_length=1, primary_key=True)
    REFEROUTHOSP: Optional[str] = Field(default=None, max_length=5)
    CAUSEOUT: Optional[str] = Field(default=None, max_length=1)
    COST: Optional[condecimal(max_digits=11, decimal_places=2)] = Field(default=None)
    PRICE: condecimal(max_digits=11, decimal_places=2)
    PAYPRICE: condecimal(max_digits=11, decimal_places=2)
    ACTUALPAY: condecimal(max_digits=11, decimal_places=2)
    D_UPDATE: datetime.datetime
    HSUB: Optional[str] = Field(default=None, max_length=5)
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)


class SpecialPp(SQLModel, table=True):
    __tablename__ = 'specialpp'

    HOSPCODE: str = Field(max_length=5, primary_key=True)
    PID: str = Field(max_length=15, primary_key=True)
    SEQ: Optional[str] = Field(default=None, max_length=16)
    DATE_SERV: datetime.date = Field(primary_key=True)
    SERVPLACE: str = Field(max_length=1, primary_key=True)
    PPSPECIAL: str = Field(max_length=6, primary_key=True)
    PPSPLACE: Optional[str] = Field(default=None, max_length=5)
    PROVIDER: Optional[str] = Field(default=None, max_length=15)
    D_UPDATE: datetime.datetime
    CID: Optional[str] = Field(default=None, max_length=13)
    HDC_DATE: Optional[datetime.datetime] = Field(default=None)
