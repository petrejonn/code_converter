from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
sys.path.append("..")
import time


class SportybetMatchScraper():
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=chrome_options)
        self._action = ActionChains(self._driver)
        with open("slip_converter/data/sportybetmatches.csv", "w") as f:
            f.write("category\ttournament\tmatch\n")
        self._driver.get("https://www.sportybet.com/ng/sport/football/")

    def scrape(self):
        cats = []
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "sport-list"))
            )
        finally:
            sport_list = self._driver.find_element_by_class_name("sport-list")
            categories = sport_list.find_elements_by_class_name("category-list-item")
            c=0
            for category in categories:
                category_item = category.find_element_by_class_name("category-item")
                cat_name = category_item.find_elements_by_tag_name("span")[0].text.strip()
                self._action.move_to_element(category).perform()
                cats.append(cat_name)
                if c > 4:
                    break
                c += 1
                # try:
                #     WebDriverWait(self._driver, 10).until(
                #         EC.presence_of_element_located(
                #             (By.CLASS_NAME, "tournament-list-item"))
                #     )
                # finally:
                #     tournaments = category.find_elements_by_class_name("tournament-list-item")
                #     for tournament in tournaments:
                #         try:
                #             WebDriverWait(self._driver, 10).until(
                #                 EC.presence_of_element_located(
                #                     (By.CLASS_NAME, "tournament-list-item"))
                #             )
                #         finally:
                #             tour_name = tournament.find_element_by_class_name("tournament-name").text.strip()
        # >>>>>>>>>> Start Scrape >>>>>>>>>>>>
        for cat in cats:
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "sport-list"))
                )
            finally:
                sport_list = self._driver.find_element_by_class_name("sport-list")
                categories = sport_list.find_elements_by_class_name("category-list-item")
                for category in categories:
                    category_item = category.find_element_by_class_name("category-item")
                    cat_name = category_item.find_elements_by_tag_name("span")[0].text.strip()
                    if cat_name != cat:
                        continue
                    self._action.move_to_element(category).perform()
                    try:
                        WebDriverWait(self._driver, 10).until(
                            EC.presence_of_element_located(
                                (By.CLASS_NAME, "tournament-list-item"))
                        )
                    finally:
                        tournaments = category.find_elements_by_class_name("tournament-list-item")
                        for tournament in tournaments:
                            try:
                                WebDriverWait(self._driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.CLASS_NAME, "tournament-list-item"))
                                )
                            finally:
                                tour_name = tournament.find_element_by_class_name("tournament-name").text.strip()
                                tournament.click()
                                time.sleep(10)
                                try:
                                    WebDriverWait(self._driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.CLASS_NAME, "match-league"))
                                    )
                                finally:
                                    league = self._driver.find_elements_by_class_name("match-league")[0]
                                    matches = league.find_elements_by_class_name("teams")
                                    for match in matches:
                                        home = match.find_element_by_class_name("home-team").text.strip()
                                        away = match.find_element_by_class_name("away-team").text.strip()
                                        match_det = cat_name+"\t"+tour_name+"\t"+home+"--v--"+away+"\n"
                                        with open("slip_converter/data/sportybetmatches.csv", "a") as f:
                                            f.write(match_det)
                        # for tournament in tournaments:
                        #     try:
                        #         WebDriverWait(self._driver, 10).until(
                        #             EC.presence_of_element_located(
                        #                 (By.CLASS_NAME, "tournament-list-item"))
                        #         )
                        #     finally:
                        #         tournament.click()
                        centre = self._driver.find_element_by_class_name("m-main-mid")
                        try:
                            WebDriverWait(self._driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.CLASS_NAME, "del-icon"))
                            )
                        finally:
                            del_icons = centre.find_elements_by_class_name("del-icon")
                            for del_icon in del_icons:
                                del_icon.click()

