import time

from screeninfo import get_monitors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import cprint
from bs4 import BeautifulSoup
from config import Config
from icecream import ic
from prettytable import PrettyTable


def browser(url):
    return Browser(url)


class Browser:
    def __init__(self, url):
        cprint(f'trying to connect to {url[8:]}')
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        if url == Config.PD_URL:
            self.site = 'pd'
            self.monitor = 0
        elif url == Config.NR_URL:
            self.site = 'nr'
            self.monitor = 1
        self.startup()
        self.page_source = self.driver.page_source

    def refresh(self):
        self.driver.refresh()

    def startup(self):
        cprint(f'{self.site} starting up')
        self.arrange()
        self.login()
        if self.site == 'nr':
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'View all (1)')))
            view_all_button = self.driver.find_element(By.LINK_TEXT, 'View all (1)')
            view_all_button.click()
        cprint(f'{self.site} started up', 'green')

    def arrange(self):
        cprint(f'moving {self.site} to {self.monitor} monitor')
        monitor = get_monitors()[self.monitor]
        if self.monitor == 0:
            self.driver.set_window_position(-monitor.width, 0, 'current')
        else:
            self.driver.set_window_position(monitor.width, 0, 'current')
        self.driver.maximize_window()
        cprint(f'window {self.site} moved and maximised')

    def login(self):  # TODO refactor too much if's
        cprint(f'authorising on {self.site}')
        login = Config.NR_LOGIN if self.site == 'nr' else Config.PD_LOGIN
        password = Config.NR_PASSWORD if self.site == 'nr' else Config.PD_PASSWORD
        login_field_ = 'login[email]' if self.site == 'nr' else 'email'
        password_field_ = 'login[password]' if self.site == 'nr' else 'password'
        login_field = self.driver.find_element(By.NAME, login_field_)
        login_field.send_keys(login)
        if self.site == 'nr':
            login_field.submit()
        password_field = self.driver.find_element(By.NAME, password_field_)
        password_field.send_keys(password)
        password_field.submit()
        cprint(f'authorised on {self.site}', 'green')

    def scrape(self):
        cprint('scrapper started')
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        errors = soup.find('div', class_='css-12m5559').findAll('tr', class_='error')
        for error in errors:
            cprint(error)


class PDScrapper:
    def __init__(self, pd_page: Browser):#, nr_page: Browser):
        self.pd_soup = BeautifulSoup(pd_page.driver.page_source, "html.parser")
        #self.nr_soup = BeautifulSoup(nr_page.driver.page_source)

    def get_data_from_pd(self):
        table = self.pd_soup.find('div', class_='react-grid-layout'
                                  ).find('div', class_='react-grid-item'
                                      ).find('div', class_='css-12m5559'
                                             ).find('div', class_='css-fasxxq'
                                                    ).find('table', class_='ui celled table')
        table_data_list = table.find_all('td')

        return table_data_list

    def view_failed_checks(self, blink: bool = False):
        data = self.get_data_from_pd()
        current_failed_checks_quantity = int(len(data) / 3)
        if blink:
            cprint('GOT NEW FAILED CHECK', 'red', attrs=['blink'])
        result = f'{time.asctime()}\n{current_failed_checks_quantity} checks are failed\n'
        pos = 1
        for td in data:
            hrefs = td.find_all('a')
            for href in hrefs:
                result += f'{"_" * 40}\n'
                result += f'| {pos} | {href.get_text()}{" " * (33 - len(href.get_text()))} |\n'
                pos += 1
        result += f' {"_" * 40}'
        return result

    def get_errors(self):
        errors = self.pd_soup.findAll('tr', class_='error')
        return errors

    def compose_table(self, errors):
        pass


class NRScrapper:
    def __init__(self, nr_page: Browser):
        self.nr_soup = BeautifulSoup(nr_page.driver.page_source, 'html.parser')

    def get_activity_stream(self):
        stream_list = self.nr_soup.findAll('div', class_='AAGMAC-wnd-ListItem')
        return stream_list



# class Scrapper:
#     def __init__(self, pd: Browser):
#         self.pd = pd
#         self.soup = BeautifulSoup(pd.page_source, 'html.parser')
#         self.scrape()
#
#     def scrape(self):
#         self.pd.refresh()
#         errors = self.soup.findAll('tr', class_='error')
#         for error in errors:
#             cprint(error)
