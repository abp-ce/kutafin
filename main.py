from __future__ import print_function
import re
from sys import argv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from frigate import Frigate
from selenium_frigate import selenium_frigate

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1HFbeHuiU_QNT45DSohVMw548EiFkgGSHyKdtafSvVXw'

def is_empty_red(st) -> bool:
    #print(st)
    arr = st.split('<td>')
    empty, red = True, False
    for i in range(len(arr)-2): 
        if not (arr[i] == '' or arr[i] == '</td>'):
            empty = False
            break
    if 'exclamation-icon.png' in arr[-1]:
        red = True
    return empty, red

def get_values(table) -> list:
    regexIP = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    hregexIP = r'<td>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}</td>'

    arr = re.findall(regexIP,table)
    tarr = re.split(hregexIP,table)
    values = []
    for i, ar in enumerate(arr):
        a = ar[ar.find('.')+1:]
        n_modem = a[a.find('.')+1:a.rfind('.')]
        empty, red = is_empty_red(tarr[i+1])
        #print(n_modem,empty,red)
        if empty: val = [n_modem,'','','кр'] if red else [n_modem,'','1','']
        else: val = [n_modem,'','','']
        values.append(val)
    print(values)
    return values

def main():
    """
    secure_file - must be your own and email for the Service Access Key must be added to access settings with edit right
    to google sheet 
    """
    is_Selenium = True if len(argv) == 1 else False

    secure_file = 'dazzling-ego-280408-24aba85079d1.json'
    tables = ['117','138','161']
    if is_Selenium: html_tables = selenium_frigate(tables)
    else: frigate = Frigate()
    #frigate.login()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    creds = service_account.Credentials.from_service_account_file(secure_file, scopes=SCOPES)

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        for i, t in enumerate(tables):
            if is_Selenium: body = {'values': get_values(table=html_tables[i])}
            else: body = {'values': get_values(table=frigate.table(t))}
            res = sheet.values().update(spreadsheetId=SPREADSHEET_ID,range=f'{t}!B3',valueInputOption="RAW",body=body).execute()
            print(res)


    except HttpError as err:
        print(err)

main()