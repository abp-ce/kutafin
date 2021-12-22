from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from frigate import Frigate

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
    driver.get("https://frigate-proxy.ru/en/type/all")

    try:
        el = driver.find_element(by='class name',value='white-saas-generator-btn-cancel')
        #el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'white-saas-generator-btn-cancel')))
    except Exception:
        print('Exception: white-saas-generator-btn-cancel')
        return None
    else: 
        time.sleep(10)
        el.click()

    try: element = driver.find_element(by='link text',value='Login')
    except Exception: 
        print('Exception: Login')
        return None
    else: element.click()
    try: email = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/div[@class="inp-w"]/input[@name="email"]'))
        )
    except Exception: 
        print('Exception: User')
        return None
    else: email.send_keys(user)

    try: passwd = driver.find_element(by='name',value='password')
    except Exception:
        print('Exception: Password')
        return None
    else: passwd.send_keys(password)

    try: google = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    except Exception:
        print('Exception: google')
        return None
    else:
        anchor = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox")))
        anchor.click()
    # Задержка на заполнение captcha
    time.sleep(40)
    driver.switch_to.default_content()
    submit = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="js_come-in"]/div[@class="popup_content"]/form[@class="popup-form"]/button[1]')))
    submit.click()
    # Задержка на получение email
    time.sleep(30)
    frigate = Frigate()
    code = frigate.email_code()
    try: ver_code = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="filter-item"]/input[1]')))
    except Exception:
        print('Exception: verification code')
        return None
    else: ver_code.send_keys(code)
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