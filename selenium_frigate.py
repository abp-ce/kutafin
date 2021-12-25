from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from frigate import Frigate

def check_iframe(driver, place):
    """
    Закрывает ws-quiz-ifame, если он есть. Возвращает True, если ws-quiz-iframe обработан.
    """
    print(f'Exception: {place}')
    try: 
        driver.switch_to.frame('ws-quiz-iframe')
        el = driver.find_element(by='class name',value='close-btn')
        el.click()
        driver.switch_to.default_content()
        return True
    except Exception:
        print('Exception: no ws-quiz-ifame')
        return False

def selenium_frigate(tables, user='dockeep9@gmail.com', password='l4}$04|G') ->str:
    """
    Реализует двухвакторную авторизацию и возвращает массив HTML таблиц (<table>...</table>) 
    для запрашиваемых таблиц в параметре tables(массив строк)
    """
    options = Options()
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-notifications")
    options.add_argument("--lang=ru")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get("https://frigate-proxy.ru/ru/type/all")
    
    try:
        el = driver.find_element(by='class name',value='white-saas-generator-btn-cancel')
    except Exception:
        if check_iframe(driver, 'white-saas-generator-btn-cancel'):
            el = driver.find_element(by='class name',value='white-saas-generator-btn-cancel')
        else: return None
    finally: 
        el.click()
    
    try: element = driver.find_element(by='xpath',value='//a[@href="come-in"]')
    except Exception: 
        if check_iframe(driver, 'Login'): element = driver.find_element(by='xpath',value='//a[@href="come-in"]')
        else: return None
    finally: element.click()

    try: email = driver.find_element(by='xpath',value='//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/div[@class="inp-w"]/input[@name="email"]')
    except Exception: 
        if check_iframe(driver, 'User'):
            email = driver.find_element(by='xpath',value='//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/div[@class="inp-w"]/input[@name="email"]')
        else: return None
    finally: email.send_keys(user)

    try: passwd = driver.find_element(by='name',value='password')
    except Exception:
        if check_iframe(driver, 'Password'): passwd = driver.find_element(by='name',value='password')
        else: return None
    finally: passwd.send_keys(password)
    
    try:
        driver.switch_to.frame(driver.find_element(by='css selector',value='iframe[src^="https://www.google.com/recaptcha/api2/anchor"]')) 
    except Exception:
        if check_iframe(driver, 'google'):
            driver.switch_to.frame(driver.find_element(by='css selector',value='iframe[src^="https://www.google.com/recaptcha/api2/anchor"]')) 
        else: return None
    finally:
        anchor = driver.find_element(by='id',value='recaptcha-anchor')
        anchor.click()
    # Задержка на заполнение captcha
    time.sleep(40)
    driver.switch_to.default_content()
    submit = driver.find_element(by='xpath',value='//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/button[1]')
    submit.click()
    # Задержка на получение email
    time.sleep(15)
    frigate = Frigate()
    code = frigate.email_code()
    try: 
        ver_code = driver.find_element(by='xpath',value='//div[@class="filter-item"]/input[1]')
    except Exception:
        if check_iframe(driver, 'verification code'):
            ver_code = driver.find_element(by='xpath',value='//div[@class="filter-item"]/input[1]')
        else: return None
    finally: ver_code.send_keys(code)
    submit = driver.find_element(by='xpath',value='//div[@class="forgot-pass-w"]/form[1]/button[1]')
    submit.click()
    time.sleep(5)

    original_window = driver.current_window_handle
    res = []
    for table in tables:
        driver.switch_to.new_window('tab')
        driver.get(f"https://frigate-proxy.ru/ru/server_modems/{table}")
        res.append(frigate.table_from_html(driver.page_source))
        driver.close()
        driver.switch_to.window(original_window)
    return res

#selenium_frigate()