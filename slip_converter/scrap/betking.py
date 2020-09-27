from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.append("..")
from time import sleep

ignor_cat = ["Champions League Special", "Special Offer","Market Transfer"]

class BetkingMatchScraper():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=chrome_options)
        with open("slip_converter/data/betkingmatches.csv", "w") as f:
            f.write("category\ttournament\tmatch\n")
        self._driver.get("https://www.betking.com/sports/s/prematch/soccer")

    def scrape(self):
        # >>>>>>>>> Close Cookie Popup >>>>>>>>>>>>
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cookieBoxClose"))
            )
        finally: 
            self._driver.find_element_by_class_name("cookieBoxClose").click()
        # >>>>>>>> Get all Categories >>>>>>>>>>>>>>
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "eventCategory"))
            )
        finally:
            categories = self._driver.find_elements_by_class_name("eventCategory")
            categories_name = []
            for category in categories:
                cat_name = category.find_element_by_class_name("itemName").text.strip()
                if cat_name in ignor_cat:
                    continue
                categories_name.append(cat_name)
            
            # >>>>>>>>> visit categories >>>>>>>>>>>>>
            for cat_name in categories_name:
                self._driver.get("https://www.betking.com/sports/s/prematch/soccer")
                try:
                    WebDriverWait(self._driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "eventCategory"))
                    )
                finally:
                    cats_ = self._driver.find_elements_by_class_name("eventCategory")
                    for cat_ in cats_:
                        if cat_name == cat_.find_element_by_class_name("itemName").text.strip():
                            cat_.click()
                            btns = self._driver.find_element_by_id("buttons")
                            btns.find_elements_by_tag_name("button")[1].click()
                            try:
                                WebDriverWait(self._driver, 10).until(
                                    EC.presence_of_element_located((By.CLASS_NAME, "eventContainer"))
                                )
                            finally:
                                events = self._driver.find_elements_by_class_name("eventContainer")
                                for event in events:
                                    title = event.find_element_by_class_name("panel-title")
                                    tour_name = title.find_elements_by_tag_name("span")[0].text.strip()
                                    matche_section = event.find_element_by_class_name("oddsLeftSection")
                                    matche_table = matche_section.find_element_by_tag_name("tbody")
                                    matches = matche_table.find_elements_by_class_name("trOddsSection")
                                    for match in matches:
                                        teams = match.find_element_by_class_name("matchName").text.strip().split(" - ")
                                        match_det = cat_name+"\t"+tour_name+"\t"+teams[0]+"--v--"+teams[1]+"\n"
                                        with open("slip_converter/data/betkingmatches.csv", "a") as f:
                                            f.write(match_det)
                            break

