from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.append("..")

class Bet9jaMatchScraper():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=chrome_options)
        with open("slip_converter/data/bet9jamatches.csv", "w") as f:
            f.write("category\ttournament\tmatch\n")
        self._driver.get("https://web.bet9ja.com/Sport/Default.aspx")

    def scrape(self):
        cat_tours = []
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nameSport"))
            )
        finally:
            category_list = self._driver.find_elements_by_class_name("nameSport")
            for category in category_list:
                if category.text.strip() == "Soccer":
                    category.click()
                    break
        # >>>>>>>> Navigate To Category>>>>>>>>>>
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nameGroup"))
            )
        finally:
            sport_group = self._driver.find_element_by_class_name("itemSport.sel")
            groups = sport_group.find_elements_by_class_name("nameGroup")
            for group in groups:
                group.click()
                # >>>>>>> Navigate to Tournament >>>>>>>>>>>>
                try:
                    WebDriverWait(self._driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "nameEvent"))
                    )
                finally:
                    events = self._driver.find_elements_by_class_name("nameEvent")
                    for event in events:
                        if event.text == "":
                            continue
                        cat_tours.append([group.text,event.text])
                group.click()


        for cat_tour in cat_tours:
            self._driver.get("https://web.bet9ja.com/Sport/Default.aspx")
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nameSport"))
                )
            finally:
                category_list = self._driver.find_elements_by_class_name("nameSport")
                for category in category_list:
                    if category.text.strip() == "Soccer":
                        category.click()
                        break
            # >>>>>>>> Navigate To Category>>>>>>>>>>
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nameGroup"))
                )
            finally:
                sport_group = self._driver.find_element_by_class_name("itemSport.sel")
                groups = sport_group.find_elements_by_class_name("nameGroup")
                for group in groups:
                    if group.text.strip() == cat_tour[0]:
                        group.click()
                        break
            # >>>>>>> Navigate to Tournament >>>>>>>>>>>>
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nameEvent"))
                )
            finally:
                events = self._driver.find_elements_by_class_name("nameEvent")
                for event in events:
                    if event.text.strip() == cat_tour[1]:
                        event.click()
                        try:
                            WebDriverWait(self._driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "Event"))
                            )
                        finally:
                            games = self._driver.find_elements_by_class_name("Event")
                            for game in games:
                                match = game.text.split(" - ")
                                home = match[0].strip()
                                away = match[1].strip()
                                match_det = cat_tour[0]+"\t"+cat_tour[1]+"\t"+home+"--v--"+away+"\n"
                                with open("slip_converter/data/bet9jamatches.csv", "a") as f:
                                    f.write(match_det)
                        break
    

