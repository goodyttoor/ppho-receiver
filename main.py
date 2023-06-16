from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from db import get_session, init_db
from model import ReceiveData, Person, DxOpd, DxIpd, OperationOpd, OperationIpd, Service, Admission

# List of allowed IP addresses
allow_ips = ['127.0.0.1', '192.168.1.1']

# Map table name from input to database
table_map = {
    'cmu_dent_person': 'person',
    'cmu_dent_dx_opd': 'dx_opd',
    'cmu_dent_dx_ipd': 'dx_ipd',
    'cmu_dent_operation_opd': 'operation_opd',
    'cmu_dent_operation_ipd': 'operation_ipd',
    'cmu_dent_service': 'service',
    'cmu_dent_admission': 'admission',
}

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
async def receive(input_obj: ReceiveData, session: Session = Depends(get_session)):
    # TODO: Check input IP address and reject unknown

    # Check known table name
    if input_obj.table_name not in table_map:
        return {'message': 'Error: Unknown table name'}

    # Get input table name
    table_name = table_map[input_obj.table_name]

    # Counters for output message
    count_new = 0
    count_update = 0

    # Loop through input data array
    for data in input_obj.data:
        new_obj = Person.parse_obj(data)

        # Check if row existed
        statement = None
        if table_name == 'person':
            statement = select(Person).where(Person.hcode == new_obj.hcode).where(Person.cid == new_obj.cid)
        elif table_name == 'dx_opd':
            statement = select(DxOpd).where(DxOpd.hcode == new_obj.hcode).where(DxOpd.cid == new_obj.cid).where(
                DxOpd.datesev == new_obj.datesev)
        elif table_name == 'dx_ipd':
            statement = select(DxIpd).where(DxIpd.hcode == new_obj.hcode).where(DxIpd.cid == new_obj.cid).where(
                DxIpd.datesev == new_obj.datesev)
        elif table_name == 'operation_opd':
            statement = select(OperationOpd).where(OperationOpd.hcode == new_obj.hcode).where(
                OperationOpd.cid == new_obj.cid).where(OperationOpd.datesev == new_obj.datesev)
        elif table_name == 'operation_ipd':
            statement = select(OperationIpd).where(OperationIpd.hcode == new_obj.hcode).where(
                OperationIpd.cid == new_obj.cid).where(OperationIpd.datesev == new_obj.datesev)
        elif table_name == 'service':
            statement = select(Service).where(Service.hcode == new_obj.hcode).where(Service.cid == new_obj.cid).where(
                Service.datesev == new_obj.datesev)
        elif table_name == 'admission':
            statement = select(Admission).where(Admission.hcode == new_obj.hcode).where(
                Admission.cid == new_obj.cid).where(Admission.datesev == new_obj.datesev)

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
    return {'message': 'Success: {} added, {} updated'.format(count_new, count_update)}


# TODO: Remove docs in production
# Redirect root to docs
@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
