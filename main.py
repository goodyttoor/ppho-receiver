from fastapi import FastAPI, Depends, Request
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from db import get_session, init_db
from model import ReceiveData, Admission, CommunityService, Dental, DiagnosisIpd, DiagnosisOpd, OcScfcIpd, OcScfcOpd, \
    PersonCid, PersonDb, ProcedureIpd, ProcedureOpd, Rehabilitation, Service, SpecialPp

# List of allowed IP addresses
allow_ips = ['127.0.0.1', '192.168.1.1']

# Map table name from input to database
tables = (
    'admission',
    'community_service',
    'dental',
    'diagnosis_ipd',
    'diagnosis_opd',
    'oc_scfc_ipd',
    'oc_scfc_opd',
    'person_cid',
    'person_db',
    'procedure_ipd',
    'procedure_opd',
    'rehabilitation',
    'service',
    'specialpp'
)

# Create FastAPI instance
app = FastAPI(
    title='PPHO Data Receiver',
    version='1.0.0'
)


@app.on_event('startup')
def on_startup():
    init_db()


# Data receiver
@app.post('/receive')
async def receive(input_obj: ReceiveData, request: Request, session: Session = Depends(get_session)):
    # Check input IP address and reject unknown
    # ip = request.client.host
    # if ip not in allow_ips:
    #     return {'message': 'Error: IP address not allow'}

    # Check known table name
    if input_obj.table_name not in tables:
        return {'message': 'Error: Unknown table name'}

    # Counters for output message
    count_new = 0
    count_update = 0

    # Loop through input data array
    for data in input_obj.data:

        # Check if row existed
        statement = None
        if input_obj.table_name == 'admission':
            new_obj = Admission.parse_obj(data)
            statement = select(Admission) \
                .where(Admission.HOSPCODE == new_obj.HOSPCODE) \
                .where(Admission.PID == new_obj.PID) \
                .where(Admission.SEQ == new_obj.SEQ) \
                .where(Admission.AN == new_obj.AN) \
                .where(Admission.DATETIME_ADMIT == new_obj.DATETIME_ADMIT) \
                .where(Admission.DATETIME_DISCH == new_obj.DATETIME_DISCH)
        elif input_obj.table_name == 'community_service':
            new_obj = CommunityService.parse_obj(data)
            statement = select(CommunityService) \
                .where(CommunityService.HOSPCODE == new_obj.HOSPCODE) \
                .where(CommunityService.PID == new_obj.PID) \
                .where(CommunityService.SEQ == new_obj.SEQ) \
                .where(CommunityService.DATE_SERV == new_obj.DATE_SERV) \
                .where(CommunityService.COMSERVICE == new_obj.COMSERVICE)
        elif input_obj.table_name == 'dental':
            new_obj = Dental.parse_obj(data)
            statement = select(Dental) \
                .where(Dental.HOSPCODE == new_obj.HOSPCODE) \
                .where(Dental.PID == new_obj.PID) \
                .where(Dental.SEQ == new_obj.SEQ) \
                .where(Dental.DATE_SERV == new_obj.DATE_SERV)
        elif input_obj.table_name == 'diagnosis_ipd':
            new_obj = DiagnosisIpd.parse_obj(data)
            statement = select(DiagnosisIpd) \
                .where(DiagnosisIpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(DiagnosisIpd.PID == new_obj.PID) \
                .where(DiagnosisIpd.AN == new_obj.AN) \
                .where(DiagnosisIpd.DATETIME_ADMIT == new_obj.DATETIME_ADMIT) \
                .where(DiagnosisIpd.WARDDIAG == new_obj.WARDDIAG) \
                .where(DiagnosisIpd.DIAGTYPE == new_obj.DIAGTYPE) \
                .where(DiagnosisIpd.DIAGCODE == new_obj.DIAGCODE)
        elif input_obj.table_name == 'diagnosis_opd':
            new_obj = DiagnosisOpd.parse_obj(data)
            statement = select(DiagnosisOpd) \
                .where(DiagnosisOpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(DiagnosisOpd.PID == new_obj.PID) \
                .where(DiagnosisOpd.SEQ == new_obj.SEQ) \
                .where(DiagnosisOpd.DATE_SERV == new_obj.DATE_SERV) \
                .where(DiagnosisOpd.DIAGTYPE == new_obj.DIAGTYPE) \
                .where(DiagnosisOpd.DIAGCODE == new_obj.DIAGCODE) \
                .where(DiagnosisOpd.CLINIC == new_obj.CLINIC)
        elif input_obj.table_name == 'oc_scfc_ipd':
            new_obj = OcScfcIpd.parse_obj(data)
            statement = select(OcScfcIpd) \
                .where(OcScfcIpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(OcScfcIpd.PID == new_obj.PID) \
                .where(OcScfcIpd.AN == new_obj.AN) \
                .where(OcScfcIpd.DATETIME_ADMIT == new_obj.DATETIME_ADMIT) \
                .where(OcScfcIpd.WARDDIAG == new_obj.WARDDIAG) \
                .where(OcScfcIpd.DIAGTYPE == new_obj.DIAGTYPE) \
                .where(OcScfcIpd.DIAGCODE == new_obj.DIAGCODE)
        elif input_obj.table_name == 'oc_scfc_opd':
            new_obj = OcScfcOpd.parse_obj(data)
            statement = select(OcScfcOpd) \
                .where(OcScfcOpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(OcScfcOpd.PID == new_obj.PID) \
                .where(OcScfcOpd.SEQ == new_obj.SEQ) \
                .where(OcScfcOpd.DATE_SERV == new_obj.DATE_SERV) \
                .where(OcScfcOpd.DIAGTYPE == new_obj.DIAGTYPE) \
                .where(OcScfcOpd.DIAGCODE == new_obj.DIAGCODE) \
                .where(OcScfcOpd.CLINIC == new_obj.CLINIC)
        elif input_obj.table_name == 'person_cid':
            new_obj = PersonCid.parse_obj(data)
            statement = select(PersonCid) \
                .where(PersonCid.person_id == new_obj.person_id)
        elif input_obj.table_name == 'person_db':
            new_obj = PersonDb.parse_obj(data)
            statement = select(PersonDb) \
                .where(PersonDb.HOSPCODE == new_obj.HOSPCODE) \
                .where(PersonDb.PID == new_obj.PID)
        elif input_obj.table_name == 'procedure_ipd':
            new_obj = ProcedureIpd.parse_obj(data)
            statement = select(ProcedureIpd) \
                .where(ProcedureIpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(ProcedureIpd.PID == new_obj.PID) \
                .where(ProcedureIpd.AN == new_obj.AN) \
                .where(ProcedureIpd.DATETIME_ADMIT == new_obj.DATETIME_ADMIT) \
                .where(ProcedureIpd.WARDSTAY == new_obj.WARDSTAY) \
                .where(ProcedureIpd.PROCEDCODE == new_obj.PROCEDCODE) \
                .where(ProcedureIpd.TIMESTART == new_obj.TIMESTART)
        elif input_obj.table_name == 'procedure_opd':
            new_obj = ProcedureOpd.parse_obj(data)
            statement = select(ProcedureOpd) \
                .where(ProcedureOpd.HOSPCODE == new_obj.HOSPCODE) \
                .where(ProcedureOpd.PID == new_obj.PID) \
                .where(ProcedureOpd.SEQ == new_obj.SEQ) \
                .where(ProcedureOpd.DATE_SERV == new_obj.DATE_SERV) \
                .where(ProcedureOpd.CLINIC == new_obj.CLINIC) \
                .where(ProcedureOpd.PROCEDCODE == new_obj.PROCEDCODE)
        elif input_obj.table_name == 'rehabilitation':
            new_obj = Rehabilitation.parse_obj(data)
            statement = select(Rehabilitation) \
                .where(Rehabilitation.HOSPCODE == new_obj.HOSPCODE) \
                .where(Rehabilitation.PID == new_obj.PID) \
                .where(Rehabilitation.DATE_SERV == new_obj.DATE_SERV) \
                .where(Rehabilitation.REHABCODE == new_obj.REHABCODE)
        elif input_obj.table_name == 'service':
            new_obj = Service.parse_obj(data)
            statement = select(Service) \
                .where(Service.HOSPCODE == new_obj.HOSPCODE) \
                .where(Service.PID == new_obj.PID) \
                .where(Service.SEQ == new_obj.SEQ) \
                .where(Service.DATE_SERV == new_obj.DATE_SERV) \
                .where(Service.INSTYPE == new_obj.INSTYPE) \
                .where(Service.TYPEIN == new_obj.TYPEIN) \
                .where(Service.SERVPLACE == new_obj.SERVPLACE) \
                .where(Service.TYPEOUT == new_obj.TYPEOUT)
        elif input_obj.table_name == 'specialpp':
            new_obj = SpecialPp.parse_obj(data)
            statement = select(SpecialPp) \
                .where(SpecialPp.HOSPCODE == new_obj.HOSPCODE) \
                .where(SpecialPp.PID == new_obj.PID) \
                .where(SpecialPp.DATE_SERV == new_obj.DATE_SERV) \
                .where(SpecialPp.SERVPLACE == new_obj.SERVPLACE) \
                .where(SpecialPp.PPSPECIAL == new_obj.PPSPECIAL)

        # Get old object
        old_obj = session.exec(statement).one_or_none()

        if old_obj is None:
            # Add new row
            session.add(new_obj)
            count_new += 1
        else:
            # Update properties
            for key, value in {k: v for k, v in new_obj.__dict__.items() if not str(k).startswith('_')}.items():
                setattr(old_obj, key, value)

            # Update existed row
            session.add(old_obj)
            count_update += 1

    # Commit to database, finger cross
    session.commit()
    return {'message': 'Success: {count_new} added, {count_update} updated'.format(count_new=count_new,
                                                                                   count_update=count_update)}


# Check incoming IP address
@app.get('/check_ip')
async def check_ip(request: Request):
    ip = request.client.host
    return {'message': 'We see your IP as {ip}'.format(ip=ip)}


# TODO: Remove docs in production
# Redirect root to docs
@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
