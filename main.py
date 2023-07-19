import os
from datetime import datetime
from typing import List

import databases
import sqlalchemy
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import RedirectResponse

# Load database config from .env file
load_dotenv()

db_url = os.environ.get('DATABASE_URL')
db_port = os.environ.get('DATABASE_PORT')
db_name = os.environ.get('DATABASE_NAME')
db_user = os.environ.get('DATABASE_USER')
db_pass = os.environ.get('DATABASE_PASS')

DATABASE_URL = 'mysql://{db_user}:{db_pass}@{db_url}:{db_port}/{db_name}'.format(
    db_url=db_url,
    db_port=db_port,
    db_name=db_name,
    db_user=db_user,
    db_pass=db_pass
)

# Create database connection
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

receive_logs = sqlalchemy.Table(
    "api_receiver_log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("hcode", sqlalchemy.Integer),
    sqlalchemy.Column("method", sqlalchemy.String),
    sqlalchemy.Column("table_name", sqlalchemy.String),
    sqlalchemy.Column("row_count", sqlalchemy.Integer),
    sqlalchemy.Column("start_time", sqlalchemy.DateTime),
    sqlalchemy.Column("end_time", sqlalchemy.DateTime),
    sqlalchemy.Column("process_time", sqlalchemy.Float),
)

# List of allowed IP addresses
allow_ips = ['127.0.0.1', '192.168.1.1']

# Create FastAPI instance
app = FastAPI(
    title='PPHO Data Receiver',
    version='1.0.0'
)


# Data receiver model
class ReceiveData(BaseModel):
    hcode: str
    table: str
    method: str
    data: List[dict]


# Database connection
@app.on_event("startup")
async def startup():
    await database.connect()


# Database disconnection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Data receiver
@app.post('/receive')
async def receive(input_obj: ReceiveData, request: Request):
    try:
        start_time = datetime.now()

        # Check input IP address and reject unknown
        # TODO: Activate this in production
        # ip = request.client.host
        # if ip not in allow_ips:
        #     return {'message': 'Error: IP address not allow'}

        query = ''
        if input_obj.method == 'insert':
            query = '''INSERT INTO {table} ({columns}) VALUES ({values})'''
        elif input_obj.method == 'replace':
            query = '''REPLACE INTO {table} ({columns}) VALUES ({values})'''

        query = query.format(
            table=input_obj.table,
            columns=', '.join(input_obj.data[0].keys()),
            values=', '.join((':' + a for a in input_obj.data[0].keys()))
        )

        await database.execute_many(query=query, values=input_obj.data)

        # Write log
        end_time = datetime.now()
        process_time = round((end_time - start_time).total_seconds(), 2)
        query = receive_logs.insert().values(hcode=input_obj.hcode, method=input_obj.method,
                                             table_name=input_obj.table, row_count=len(input_obj.data),
                                             start_time=start_time, end_time=end_time, process_time=process_time)
        await database.execute(query=query)

        return {'message': 'Success'}

    except Exception as error:
        return {'message': 'Error: {error}'.format(error=error)}
    

# Check incoming IP address
@app.get('/check_ip')
async def check_ip(request: Request):
    ip = request.client.host
    return {'message': 'We see your IP as {ip}'.format(ip=ip)}


# Redirect root to docs
@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
