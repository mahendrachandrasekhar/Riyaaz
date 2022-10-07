import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import pandas as pd

def get_gsheet(sheetname):
    gsheet = sh.worksheet(sheetname)
    d=gsheet.get_all_records()
    return pd.DataFrame(data=d)

def set_gsheet(sheetname,data):
    gsheet = sh.worksheet(sheetname)
    gsheet.append_row(data)

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_file('.config/gspread/service_account.json')

scoped_credentials = credentials.with_scopes(
    ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']
    )
gc = gspread.Client(auth=scoped_credentials)
gc.session = AuthorizedSession(scoped_credentials)
sh = gc.open("Riyaaz Feedback")
