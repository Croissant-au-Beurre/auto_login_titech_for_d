from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from dotenv import load_dotenv, find_dotenv
import os

from data.matrix_data import MatrixCodeData

class RpaAutoLoginUsecase:
    def __init__(self) -> None:
        load_dotenv(find_dotenv())
        self.id = os.environ.get('ID')
        self.pw = os.environ.get('PW')

    def handle(self) -> list:
        """
        Automatically login into D's TiTech account
        """
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')

        browser = webdriver.Chrome(options=options)
        browser.get('https://portal.nap.gsic.titech.ac.jp/GetAccess/Login?Template=userpass_key&AUTHMETHOD=UserPassword')

        # The first pw
        id_input = browser.find_element(By.NAME, 'usr_name')
        id_input.send_keys(self.id)
        pw_input = browser.find_element(By.NAME, 'usr_password')
        pw_input.send_keys(self.pw)
        sleep(2)

        ok_btn = browser.find_element(By.NAME, 'OK')
        ok_btn.click()
        sleep(1)

        # Get the coordinates
        coordinates_dict = {}
        first_coordinate = browser.find_element(By.XPATH, '//*[@id="authentication"]/tbody/tr[6]/th[1]').text
        first_coordinate_list = self.get_coordinate(first_coordinate)
        coordinates_dict[1] = first_coordinate_list

        second_coordinate = browser.find_element(By.XPATH, '//*[@id="authentication"]/tbody/tr[7]/th[1]').text
        second_coordinate_list = self.get_coordinate(second_coordinate)
        coordinates_dict[2] = second_coordinate_list

        third_coordinate = browser.find_element(By.XPATH, '//*[@id="authentication"]/tbody/tr[8]/th[1]').text
        third_coordinate_list = self.get_coordinate(third_coordinate)
        coordinates_dict[3] = third_coordinate_list

        # The matrix pw
        matrix_data = MatrixCodeData(coordinates_dict=coordinates_dict)
        matrix_codes = matrix_data.matrix_code

        # Input codes
        first_input = browser.find_element(By.NAME, 'message4')
        first_input.send_keys(matrix_codes[0])

        second_input = browser.find_element(By.NAME, 'message5')
        second_input.send_keys(matrix_codes[1])

        third_input = browser.find_element(By.NAME, 'message6')
        third_input.send_keys(matrix_codes[2])

        # Press OK
        ok_btn = browser.find_element(By.NAME, 'OK')
        ok_btn.click()

        is_browser_open = True
        while is_browser_open:
            try:
                # Wait for user close the browser window
                WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.XPATH, "//body")))
            except:
                is_browser_open = False
                print('close')

        # Close WebDriver
        browser.quit()
        print('closed')

    def get_coordinate(self, coordinate_string:str) -> list:
        # 去除字符串中的方括号和逗号，并将其拆分为单独的元素
        elements = coordinate_string.strip('[]').split(',')

        # 将字符串元素转换为列表
        result_list = [x.strip() if i != 1 else int(x.strip()) for i, x in enumerate(elements)]

        return result_list
