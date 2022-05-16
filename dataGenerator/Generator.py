import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

class Generator:
    def __init__(self) -> None:
        self.open_driver()

    def get_screen(self, code: string) -> None:
        self.driver.get('file:///D:/workspace/capstone-design-img2code/dataGenerator/data/code/{}.html'.format(code))

        width = self.driver.execute_script("return document.body.scrollWidth") #스크롤 할 수 있는 최대 넓이
        height = self.driver.execute_script("return document.body.scrollHeight") #스크롤 할 수 있는 최대 높이
        self.driver.set_window_size(width, height) #스크롤 할 수 있는 모든 부분을 지정
        
        self.driver.save_screenshot('dataGenerator/file/img/{}.png'.format(code))

    def open_driver(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')

        self.driver = webdriver.Chrome('dataGenerator/chromedriver.exe', options=options)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(1)
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)

    def make_code(self, cnt: int) -> None:
        for filename in range(cnt):
            
            self.get_screen(filename)



if __name__=='__main__':
    g = Generator()