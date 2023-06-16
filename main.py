from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from db import get_session, init_db
from model import ReceiveData, Person

allow_ips = ['127.0.0.1', '192.168.1.1']

table_map = {
    'cmu_dent_person': 'person',
}

app = FastAPI(
    title='PPHO Data Receiver',
    version='1.0.0'
)


@app.on_event("startup")
def on_startup():
    init_db()


# Data receiver
@app.post("/receive")
async def receive(input_obj: ReceiveData, session: Session = Depends(get_session)):
    # TODO: Check input IP address and reject unknown

    # Check known table name
    if input_obj.table_name not in table_map:
        return {"message": "Error: Unknown table name"}

    # Get input table name
    table_name = table_map[input_obj.table_name]

    if table_name == 'person':
        count_new = 0
        count_update = 0

        for data in input_obj.data:
            new_person = Person.parse_obj(data)

            # Get existed person
            statement = select(Person).where(Person.hcode == new_person.hcode).where(Person.cid == new_person.cid)
            old_person = session.exec(statement).one_or_none()

            if old_person is None:
                # Add new row
                session.add(new_person)
                count_new += 1
            else:
                # Update values
                for key, value in {k: v for k, v in new_person.__dict__.items() if not str(k).startswith("_")}.items():
                    setattr(old_person, key, value)

                # Update row
                session.add(old_person)
                count_update += 1

        # Commit to database, finger cross
        session.commit()
        return {"message": "Success: {} added, {} updated".format(count_new, count_update)}

    # Something somewhere went horribly wrong T_T
    return {"message": "Error: Something went wrong"}


# Redirect root to docs
# TODO: Remove docs in production
@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
