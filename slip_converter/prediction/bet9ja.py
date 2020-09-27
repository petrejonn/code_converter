from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import market


class Bet9jaMarketMixin(object):
    def _openMatch(self)->None:
        # >>>>>Navigate to Soccer>>>>>>>>
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
            groups = self._driver.find_elements_by_class_name("nameGroup")
            for group in groups:
                if group.text.strip() == self._matchCategory:
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
                if event.text.strip() == self._matchTournament:
                    event.click()
                    break

        # >>>>>> Navigate to Game >>>>>>>>>>>>>>
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Event"))
            )
        finally:
            games = self._driver.find_elements_by_class_name("Event")
            for game in games:
                if game.text.strip() == self._game[0] + " - " + self._game[1]:
                    game.click()
                    break


class OneXTwo(Bet9jaMarketMixin, market.OneXTwo):
    @property
    def shortCode(self)->str:
        return "1X2"

    def predict(self, prediction: str)->None:
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "SEItem"))
            )
        finally:
            markets = self._driver.find_elements_by_class_name("SEItem")
            for market in markets:
                market_text = market.find_element_by_class_name("SECQ").text.strip()
                if market_text ==  self.shortCode:
                    preds = market.find_elements_by_class_name("SEOdd.g1")
                    for pred in preds:
                        if pred.find_element_by_class_name("SEOddsTQ").text == self._prediction:
                            pred.find_element_by_class_name("SEOddLnk").click()
                            break
    