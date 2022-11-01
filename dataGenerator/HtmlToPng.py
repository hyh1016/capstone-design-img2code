from posixpath import abspath
import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time

# html to img
class HtmlToPng:
    def __init__(self) -> None:
        self.open_driver()

    # path: 절대경로 입력
    def get_screen(self, path: string, file_name) -> None:
        self.driver.get('file:///{}/{}.html'.format(path, file_name))
        self.driver.implicitly_wait(10)

        #초기 너비 지정
        self.driver.set_window_size(2400, 1700)
        self.driver.execute_script("document.body.style.zoom = '3'")
        # width = self.driver.execute_script("return document.body.scrollWidth") #스크롤 할 수 있는 최대 넓이
        # height = self.driver.execute_script("return document.body.scrollHeight") #스크롤 할 수 있는 최대 높이
        #스크롤 할 수 있는 모든 부분을 지정
        # self.driver.set_window_size(width, height)
        
        self.driver.save_screenshot('dataGenerator/data/png/{}.png'.format(file_name))

    def open_driver(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path='dataGenerator/chromedriver', options=options)
        self.driver.delete_all_cookies()
        self.driver.implicitly_wait(1)
        self.driver.set_page_load_timeout(10)
        self.driver.set_script_timeout(10)
        self.driver.set_window_size(2400, 1700)

    def make_code(self, cnt: int) -> None:
        for filename in range(cnt):
            
            self.get_screen(filename)



if __name__=='__main__':
    # g = Generator()
    g = HtmlToPng()
    print(abspath('dataGenerator/data/html'))
    g.get_screen(abspath('dataGenerator/data/html'), '0')