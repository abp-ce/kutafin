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
    """
    Логика скрипта. Возвращает два логических значения - пусто и красный (значок)
    Script logic. Return two boolean values.
    """
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
    """
    Возвращает массив строк для обновления google таблицы 
    Return strings array for updating google sheet 
    """
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
    #print(values)
    return values

def main():
    """
    Заполняет google таблицу. Secure file оставил свой.
    Secure_file - must be your own and email for the Service Access Key must be added to access settings with edit right
    to google sheet 
    """
    is_Selenium = True if len(argv) == 1 else False

    secure_file = 'dazzling-ego-280408-24aba85079d1.json'
    tables = ['117','138','161']
    if is_Selenium: html_tables = selenium_frigate(tables)
    else: frigate = Frigate()
    
    # Login is not really needed. We need id and secret for modem page request.
    # We can get id and secret form login or simply view the values in the browser in developer mode.
    # Values are rarely changed.
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
        data = []
        for i, t in enumerate(tables):
            if is_Selenium: data.append({'range': f'{t}!B3', 'values': get_values(table=html_tables[i])})
            else: data.append({'range': f'{t}!B3', 'values': get_values(table=frigate.table(t))})
        body = {'valueInputOption': 'RAW', 'data': data}
        res = sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
        print(res)
        # Conditional formatting
        sheets_ids = [0, 1292097999, 729629251]
        requests = []
        for id in sheets_ids:
            ranges = [{'sheetId': id, 'startRowIndex': 2, 'startColumnIndex': 3, 'endColumnIndex': 4}]
            requests.append({
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': ranges,
                        'booleanRule': {
                            'condition': {'type': 'NOT_BLANK'},
                            'format': {'backgroundColor': {'red': 0.1, 'green': 0.6, 'blue': 0.6}
                            }
                        }
                    },
                    'index': 0
                }
            })
        res = sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body={'requests': requests}).execute()
        print(res)


    except HttpError as err:
        print(err)

main()