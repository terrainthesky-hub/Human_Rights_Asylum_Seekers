import pandas as pd
import dotenv
from pdfminer.high_level import extract_text
import os
from pathlib import Path
import os
from fastapi import FastAPI
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span 


app = FastAPI()

@app.get("/upload/pdf")
def text_scraper(pdf):
    global text
    text = extract_text(pdf)

    return text

df = pd.read_csv('judges_appointed.csv')

# filename = file.filename
# path = 'app/'+file.filename

text_scraper('163798690-Artemio-Guzman-Rodriguez-A200-234-211-BIA-Aug-23-2013.pdf')

@app.get("/upload/pdf")
def matcher(text):
    # initialize the matcher
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    matcher = Matcher(nlp.vocab)

    # Add the pattern to the matcher 

    pattern = [{"ENT_TYPE": "PERSON"}, {"ENT_TYPE": "PERSON"}]
    matcher.add("judge name", None, pattern) # 2nd argument is an optional callback


    # call the matcher on the doc 
    matches = matcher(doc)
    #checking if matches is empty
    if matches == []:
        pattern = [{"ENT_TYPE": "PERSON"}, {"ENT_TYPE": "PERSON"}, {"ORTH": ","}, {"ENT_TYPE": "PERSON"} ]
        matcher.add("judge name", None, pattern) # 2nd argument is an optional callback 
        matches = matcher(doc)

    names_list = []

    #creating a list of judge names

    for _, start, end in matches:
        matched_span = doc[start:end]
        names_list.append(matched_span.text)

    #searching our judge dataset for judge name

    for x in range(len(names_list)):
        if df['name'].str.contains(names_list[x]).any():
            judge = x
            break
        else:
            continue


    # making a dataframe with the judge name and taking the first index
    # which is where the judge name will be

    judge_name = names_list[judge]
    df1 = df[df['name'].str.contains(judge_name)]

    judge_name_final = df1['name'].iloc[0]
    print(judge_name_final)

matcher(text)