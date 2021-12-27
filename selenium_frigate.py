from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from frigate import Frigate

def try_exc(driver, by, value, place, keys = None):
    """
    Проверяет доступность элемента, если не доступен, проверяет и закрывает
    ws-quiz-ifame и наконец обрабатывает начальный элемент
    """
    try:
        el = driver.find_element(by=by,value=value)
    except Exception:
        if check_iframe(driver, place):
            el = driver.find_element(by=by,value=value)
        else: return None
    finally:
        if keys: el.send_keys(keys)
        else: el.click()
    return "Done"

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
    #options.add_argument('disable-infobars')
    #options.add_argument("--disable-notifications")
    #options.add_argument("--lang=ru")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get("https://frigate-proxy.ru/ru/type/all")
    
    if try_exc(driver, 'class name', 'white-saas-generator-btn-cancel', 'white-saas-generator-btn-cancel') == None: return None
        
    if try_exc(driver, 'xpath', '//a[@href="come-in"]', 'Login') == None: return None

    if try_exc(driver, 'xpath', '//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/div[@class="inp-w"]/input[@name="email"]', 
        'User', user) == None: return None
    
    if try_exc(driver, 'name', 'password', 'Password', password) == None: return None

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

    if try_exc(driver, 'xpath', '//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/button[1]', 'Submit 1') == None: return None

    # Задержка на получение email
    time.sleep(15)
    frigate = Frigate()
    code = frigate.email_code()

    if try_exc(driver, 'xpath', '//div[@class="filter-item"]/input[1]', 'Verification code', code) == None: return None

    if try_exc(driver, 'xpath', '//div[@class="forgot-pass-w"]/form[1]/button[1]', 'Submit 2') == None: return None

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