import re
from fastapi import FastAPI

app = FastAPI()


#the input file must have the date as Month-Day-Year in the file name

@app.get("/upload/pdf")
def date_conversion(pdf):
    date = str(pdf)

    pattern = '((?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?)(\d{1,2}(st|nd|rd|th)?)?((\s*[,.\-\/]\s*)\D?)?\s*((19[0-9]\d|20\d{2})|\d{2})*'

    dates = re.search(pattern, date)
    date_converted = (dates.group())
    print(date_converted)
    return date_converted

date_conversion(file.filename)