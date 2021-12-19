import time
import imaplib
import email
import requests

class Frigate:
    """
    Provide access to https://frigate-proxy.ru/
    """
    def __init__(self, user='dockeep9@gmail.com', password='l4}$04|G') -> None:
        self.user = user
        self.password = password
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0', 
                        'Referer': 'https://frigate-proxy.ru/ru/type/all', 
                        'Host': 'frigate-proxy.ru',
                        'Origin': 'https://frigate-proxy.ru',
                        'Accept': '*/*',
                        #'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin',
                        #'Sec-Fetch-User': '?1',
                        'TE': 'trailers',
                        #'Upgrade-Insecure-Requests': '1'
                        'X-Requested-With': 'XMLHttpRequest'
                    }
        self.cookies = { '__ddg1': 'DmIqzcmiQU48mUKecMAn', 'PHPSESSID': '36slubbsudum2o91as95ntfqp0', 'lang': 'ru',
                        '_ym_uid': '1639645763231440132',  '_ym_d': '1639645763', '_ym_isad': '2', 'WhiteCallback_visit': '15860318948',
                        'WhiteCallback_openedPages': 'pWHXE.DnvBH.qTuHl.uYDaj.HYDOo.SToUG.JtElB', 'WhiteCallback_timeAll': '25363',
                        'WhiteCallback_timePage': '25363', 'WhiteGenerator_89543_counter': 'false', 'WhiteGenerator_closed_89543': 'true',
                        'WidgetChat_invitation_2975690': 'true', 'WhiteQuiz_show_57938': 'onexit', 'WhiteQuiz_noShowWindow': '1',
                        'WhiteCallback_updateMainPage': 'pWHXE', 'WhiteCallback_visitorId': '8925594854', 'WhiteSaas_uniqueLead': 'no',
                        'WhiteCallback_mainPage': 'JtElB'}

    def login(self):
        url = 'https://frigate-proxy.ru/req/form.php'
        data = { 'act': 'form', 'email': self.user, 'password': self.password, 'lang': 'ru', 'section': 'auth', 
                'g-recaptcha-response':'03AGdBq26IIQeKaVUDkWm5X23JIVRksApqpNSoNJ_a6OrQdyT3PWrt-A1Y-DDmZpjiGLHDtyOqDCewmVTKgNkgtnghptbO-yE0HHTjRECfXisqhXnlYViUkXnK4Gz2LQfZpShHu7y2nJpsZipWUcS3ef6Hl4jYFCqSLhxi07-SN1ibXYrI2FIjbWzg4iT5hcWE5IuXCpzrlmy-6C0zpOQJa5yUyR7SYd6QOk0zMgs2eQQfhUX9q_TF53bpnnj5mN_N_qm9sVMAgJiuNJ3GT5pPD77oL0NscT7GB-Cb_30VbViJ2ihzWKT6dmwXihRFuyQU1jKOdZzpJVFbAQx838v8SsFubDmzGU70SglPxYqL_XnKRWtWx5mxA_pvq6oMH2giEDXITHxq0Nv8hmOHNt4Y3o-sWmL3vNfd1xvwVBe33T6LoGHQNPeOnwsqheG'}
        r = requests.post(url, headers=self.headers, cookies=self.cookies, data = data)
        print(r.text)
        time.sleep(20)
        pos = r.text.rfind('/')
        code_login = r.text[pos+1:].strip('"')
        print(code_login)
        data =  {'code_login': code_login, 'lang': 'ru', 'last_code': self.email_code(), 'section': 'auth_admin', 'token': ''}
        print(data)
        r = requests.post(url, headers=self.headers, cookies=self.cookies, data = data)
        print(r.text)
        print(r.cookies)
    
    def email_code(self) -> str:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(self.user, self.password)
        mail.select("inbox")
        result, data = mail.search(None, '(FROM "sapport@frigate-proxy.ru")')
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        if email_message.is_multipart():
            for payload in email_message.get_payload():
                body = payload.get_payload(decode=True).decode('utf-8')
                return body.split()[-1]
        else:    
            body = email_message.get_payload(decode=True).decode('utf-8')
            return body.split()[-1]

    def table_from_html(self, html):
        pos = html.find('<h2 class="page-title">Статус модемов по серверу')
        epos = html.find('<button type="button" class="proxy-btn">Купить прокси</button>')
        text = html[pos:epos]
        pos = text.find('<table>')
        epos = text.rfind('</table>')
        return text[pos:epos+8]
       
    
    def table(self, table) -> str:
        url = f'https://frigate-proxy.ru/ru/server_modems/{table}'
        #self.headers['Cookie'] = '__ddg1=DmIqzcmiQU48mUKecMAn; PHPSESSID=36slubbsudum2o91as95ntfqp0; lang=ru; _ym_uid=1639645763231440132; _ym_d=1639645763; WhiteCallback_visit=15846147641; WhiteCallback_openedPages=pWHXE.DnvBH.qTuHl.uYDaj.HYDOo; WhiteCallback_timeAll=27304; WhiteCallback_timePage=27304; WhiteGenerator_89543_counter=false; WhiteGenerator_closed_89543=true; WidgetChat_invitation_2975690=true; WhiteQuiz_show_57938=onexit; WhiteQuiz_noShowWindow=1; WhiteCallback_updateMainPage=pWHXE; WhiteCallback_visitorId=8925594854; WhiteSaas_uniqueLead=no; _ym_isad=2; id=8390147; secret=3f7bd7efaae16'
        print(self.headers)
        self.cookies['id'] = '8390147'
        self.cookies['secret'] ='3f7bd7efaae16'
        r = requests.get(url=url, headers=self.headers, cookies=self.cookies)
        """
        pos = r.text.find('<h2 class="page-title">Статус модемов по серверу')
        epos = r.text.find('<button type="button" class="proxy-btn">Купить прокси</button>')
        text = r.text[pos:epos]
        pos = text.find('<table>')
        epos = text.rfind('</table>')
        """
        return self.table_from_html(r.text)
