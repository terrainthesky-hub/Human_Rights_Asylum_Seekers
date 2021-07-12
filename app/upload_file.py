# All Required Imports
from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
import pandas
import urllib.request
import logging
import boto3
from botocore.config import Config
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from botocore.exceptions import ClientError
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv
import os
import aiofile
from starlette.responses import FileResponse
from fnmatch import fnmatch

# loads secret credentials 
load_dotenv()
# Connect POST request ot the api routor
router = APIRouter()

# parse case_url and scrape relivent data off of it
def case_urls(str):
    # case url data for web to no name of document on S3 buckets to view
    case_url = str
    index = str[-19:-4].find('-')
    hearing_date = str[(len(str)-19):-4]
    hearing_date = hearing_date[index+1:]
    decision_date = hearing_date
    index = str.find('-')
    indexend = str.find(hearing_date)
    a = str[indexend-8:indexend-1].find('-') +1
    str[indexend-8+a:indexend-1]
    department=str[indexend-8+a:indexend-1]
    b = str.find(department)
    c=str[:b].find('-')+1
    urlforloop = str[c:indexend-9+a]
    l = []
    for i in range(7,len(urlforloop)):
        if str[i:i+1].find('-') == -1 and str[i+2:i+3].isnumeric():
            l.append(i)
    h= min(l) - 10
    case_id = urlforloop[h:]
    t = urlforloop.find(case_id)
    refugee = urlforloop[:t+1]
    return case_id, case_url,hearing_date,decision_date,department,refugee


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None]
) -> None:
    tmp_path = save_upload_file_tmp(upload_file)
    try:
        handler(tmp_path)  # Do something with the saved temp file
    finally:
        tmp_path.unlink()  # Delete the temp file


# file uploaders
@router.post("/upload/pdf")
async def pdf(file: UploadFile = File(...)):
    filename = file.filename
    if len(filename) >= 1:
        # add these varibles to table's scrapes all the data we need from initional upload
        case_id, case_url,hearing_date, decision_date, department, refugee = case_urls(file.filename)
        # helper functions to handle file correctly
        #save_upload_file_tmp(file)
        #handle_upload_file(file, tmp_path)
        # Uploads File to S3 and downloads to scipts folder
        path = 'app/'+file.filename
        key = os.getenv('access_key')
        secret_access_key = os.getenv('secret_access_key')
        with open(path, 'wb') as file_object:
            shutil.copyfileobj(file.file, file_object)
        s3 = boto3.resource(
            's3',
            aws_access_key_id = key,
            aws_secret_access_key = secret_access_key,
            config = Config(signature_version ='s3v4')
        )
        data = open(path, 'rb')
        s3.Bucket('hrf-asylum-dsa-documents').put_object(Key='pdf/'+file.filename, Body=data)
        # scipts to scrape pdf into free text amd get judge name
        
        
        # scipt to delete pdf after being scraped
        for dirpath, dirnames, filenames in os.walk(os.curdir):
            for file in filenames:
                if fnmatch(file, '*.pdf'):
                    os.remove(os.path.join(dirpath, file))
    return {"filename": case_url,
            "case_id" : case_id,
            "case_url" : case_url,
            "hearing_date" : hearing_date,
            "decision_date" : decision_date,
            "department": department,
            "refugee": refugee,
            "s3": "Viewable"}

# deals with data from csv
def csv_data(df):
    return ""


# This route is not working yet, so don't include it
# @router.post("/upload/file")
async def not_pdf(file: UploadFile = File(...)):
            #if len(file.filename) >= 1:
    # add these varibles to table's
    #df = pd.read_csv(file)
    #varibles = csv_data(df)
    return {"filename": file.filename}


# This route is not working yet, so don't include it
# @router.post("/connect/db")
async def get_db() -> sqlalchemy.engine.base.Connection:
    """Get a SQLAlchemy database connection.
    grab this from group b due to are database not working and nobody connect the scipts and tables together
    Uses this environment variable if it exists:  
    DATABASE_URL=dialect://user:password@host/dbname
    Otherwise uses a SQLite database for initial local development.
    """
    database_url = os.getenv('DATABASE_URL')
    engine = sqlalchemy.create_engine(database_url)
    connection = engine.connect()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield connection
    finally:
        connection.close()
# the postgres database has never work yet
# load_dotenv()
# database_url = os.getenv('DATABASE_URL')
# engine = sqlalchemy.create_engine(database_url, pool_pre_ping=True)
# connection = engine.connect()
# session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
Base = declarative_base()