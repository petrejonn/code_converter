from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import market


ignor_cat = ["Champions League Special", "Special Offer"]

class BetkingMarketMixin(object):
    def _openMatch(self)->None:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "eventCategory"))
            )
        finally:
            cats_ = self._driver.find_elements_by_class_name("eventCategory")
            for cat_ in cats_:
                cat_name = cat_.find_element_by_class_name("itemName").text.strip()
                if cat_name in ignor_cat:
                    continue
                if self._matchCategory == cat_name:
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
                            if tour_name == self._matchTournament:
                                matches = event.find_elements_by_class_name("trOddsSection")
                                for match in matches:
                                    mtch = match.find_element_by_class_name("matchName")
                                    teams = mtch.find_element_by_tag_name("span").text.strip().split(" - ")
                                    if teams[0] == self._game[0] and teams[1] == self._game[1]:
                                        self._matchWebElement = match.find_element_by_class_name("oddItem.moreOdds").click()
                                        break
                                break
                    break
                        

class OneXTwo(BetkingMarketMixin, market.OneXTwo):
    @property
    def shortCode(self)->str:
        return "1X2"

    def predict(self, prediction: str)->None:
        pred = {
            "Home": "0",
            "Draw": "1",
            "Away": "2",
        }.get(self._prediction)
        self._matchWebElement.find_element_by_class_name("eventOdd-"+pred).click()

class DoubleChance(BetkingMarketMixin, market.DoubleChance):
    @property
    def shortCode(self)->str:
        return "Double Chance"

    def predict(self, prediction: str)->None:
        pass

class GGNG(SportybetMarketMixin, market.DoubleChance):
    @property
    def shortCode(self)->str:
        return "GG/NG"

    def predict(self, prediction: str)->None:
        pass

class FirstGoal(SportybetMarketMixin, market.FirstGoal):
    @property
    def shortCode(self)->str:
        return "First Goal"

    def predict(self, prediction: str)->None:
        pass

class LastGoal(SportybetMarketMixin, market.LastGoal):
    @property
    def shortCode(self)->str:
        return "Last Goal"

    def predict(self, prediction: str)->None:
        pass

class DN (SportybetMarketMixin, market.DNB):
    @property
    def shortCode(self)->str:
        return "DNB"

    def predict(self, prediction: str)->None:
        pass

class HNB(SportybetMarketMixin, market.HNB):
    @property
    def shortCode(self)->str:
        return "HNB"

    def predict(self, prediction: str)->None:
        pass

class ANB(SportybetMarketMixin, market.ANB):
    @property
    def shortCode(self)->str:
        return "ANB"

    def predict(self, prediction: str)->None:
        pass

class Handicap01(SportybetMarketMixin, market.Handicap01):
    @property
    def shortCode(self)->str:
        return "Handicap 1:0"

    def predict(self, prediction: str)->None:
        pass