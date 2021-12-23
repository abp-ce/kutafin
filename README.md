# kutafin
### $git clone https://github.com/abp-ce/kutafin.git
### $cd kutafin
### $python3 -m venv venv
### $source venv/bin/activate
### $pip install -r requirements.txt
### В директорию kutafin Вам нужно поместить Ваш Service Access Key (json) и
### chromdriver, соответствующий Вашей версии браузера и операционной системе (ссылка на скачивание 
### https://chromedriver.storage.googleapis.com/index.html).
### Google sheets файл  https://docs.google.com/spreadsheets/d/1HFbeHuiU_QNT45DSohVMw548EiFkgGSHyKdtafSvVXw/edit#gid=0
### должен иметь разрешение для редактирования для email Вашего Service Access Key.
### Запуск: 
### $python main.py <параметр>
### Если запустить без параметра - будет работать через Selenium.
### Разрабатывалось под https://frigate-proxy.ru/en/type/all, 
### c https://frigate-proxy.ru/ru/type/all не проверял.
### Если с параметром - то напрямую через requests. Параметр - любая строка или число.
