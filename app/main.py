"""This is where we bring all the modular components together."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .database import engine
import sqlalchemy
from . import models, schemas, routes, database, upload_file

# to create our models in the databse
models.Base.metadata.create_all(bind=engine)

description = """
**Human Rights First Asylum**
To use these interactive docs:
- Click on an endpoint below
- Click the **Try it out** button
- Edit the Request body or any parameters
- Click the **Execute** button
- Scroll down to see the Server response Code & Details
"""

app = FastAPI(
    title = "Human Rights First Asylum API",
    description = description,
    docs_url='/',
)

# These routes aren't working yet, so don't include them
# app.include_router(routes.router)

app.include_router(upload_file.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


if __name__ == "__main__":
    uvicorn.run(app)