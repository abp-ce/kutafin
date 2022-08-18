from __future__ import print_function

from sys import argv

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from frigate import Frigate
from selenium_frigate import selenium_frigate

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1HFbeHuiU_QNT45DSohVMw548EiFkgGSHyKdtafSvVXw'


def main():
    """
    Заполняет google таблицу. Secure file должен быть свой и email от
    Service Access Key должен быть добавлен в список кому разрешено
    править файл.
    Secure_file - must be your own and email for the Service Access Key must
    be added to access settings with edit right to google sheet.
    """
    is_Selenium = True if len(argv) == 1 else False

    secure_file = 'sf.json'
    tables = ['117', '138', '161']
    if is_Selenium:
        html_tables = selenium_frigate(tables)
        if html_tables is None:
            print('Ошибка: Не удалось получить получить таблицы')
            return
    else:
        frigate = Frigate()
        # Login is not really needed. We need id and
        # secret for modem page request.
        # We can get id and secret form login or simply view the values
        # in the browser in developer mode. Values are rarely changed.
        # frigate.login()
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        secure_file,
        scopes=SCOPES
    )

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        data = []
        for i, t in enumerate(tables):
            if is_Selenium:
                data.append({'range': f'{t}!B3', 'values': html_tables[i]})
            else:
                data.append({'range': f'{t}!B3', 'values': frigate.table(t)})
        body = {'valueInputOption': 'RAW', 'data': data}
        res = sheet.values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print((
            f'Обновлено: {res["totalUpdatedCells"]} ячеек'
            f' на {res["totalUpdatedSheets"]} листах'
        ))
        # Conditional formatting
        sheets_ids = [0, 1292097999, 729629251]
        requests = []
        for id in sheets_ids:
            ranges = [{
                'sheetId': id,
                'startRowIndex': 2,
                'startColumnIndex': 3,
                'endColumnIndex': 4
            }]
            requests.append({
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': ranges,
                        'booleanRule': {
                            'condition': {'type': 'NOT_BLANK'},
                            'format': {
                                'backgroundColor': {
                                    'red': 0.1,
                                    'green': 0.6,
                                    'blue': 0.6
                                }
                            }
                        }
                    },
                    'index': 0
                }
            })
        res = sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': requests}
        ).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
