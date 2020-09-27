import sys
sys.path.append("..")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from slip_converter.bookmakers.core import BookMaker
from slip_converter.game import FootBallGame
from slip_converter.support import marketFactory, serializePrediction
from time import sleep


class Betking():
    def __init__(self):
        self._footBallBaseUrl = "https://www.betking.com/sports/s/prematch/soccer"
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        # self._driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self._driver = webdriver.Chrome(options=chrome_options)
        self._action = ActionChains(self._driver)
        self._reloadBaseUrl()
        self._betslipGames = []

    def _bookGame(self, game: tuple) -> None:
        game_ = game[0] # tuple
        market = game[1].lower() # string
        pred_ = serializePrediction(game[2]) # string
        market_type = marketFactory(market, "betking")
        print("")
        prediction = market_type(
            pred_, self._driver, game_, self._action, 'data/betkingmatches.csv')
        game = FootBallGame(game_[0], game_[1], pred_, prediction)
        game.makePrediction()

    def bookGames(self, games: tuple) -> None:
        for game in games:
            self._bookGame(game)

    def getBookingCode(self) -> str:
        """
        @return: BetSlip Code
        """
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bookBet"))
            )
        finally:
            self._driver.find_element_by_class_name("bookBet").click()
            try:
                WebDriverWait(self._driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "couponBookedCode"))
                )
            finally:
                code_area = self._driver.find_element_by_id("couponBookedCode")
                return code_area.find_elements_by_tag_name("span")[1].text.strip()

    @classmethod
    def loadCode(cls, code: str) -> tuple:
        """
        @return: tuple of games
        """
        instance = cls()
        instance._insertCode(code)
        return instance.getBookingGames()

    def _insertCode(self, code: str) -> None:
        """
        @Desc: Insert code into betslip input field of Site
        """
        self._reloadBaseUrl
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.ID, "loadBookedCouponCode"))
            )
        finally:
            self._driver.find_element_by_id("loadBookedCouponCode").send_keys(code)
            self._driver.find_element_by_id("btnLoadBookedCoupon").click()


    def getBookingGames(self) -> tuple:
        """
        @return: A tuple of all the games in the betslip
        """
        self._serializeBetslipGames()
        return tuple(self._betslipGames)

    def _reloadBaseUrl(self,) -> None:
        """
        @Desc: re-initialize content of base page
        """
        self._driver.get(self._footBallBaseUrl)
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cookieBoxClose"))
            )
            self._driver.find_element_by_class_name("cookieBoxClose").click()
        except:
            pass

    def _serializeBetslipGames(self) -> None:
        """
        @Desc: create a Game Object of all games in betslip
        """
        self._betslipGames = []
        try:
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tblCouponEvents"))
            )
        finally:
            games =  self._driver.find_elements_by_class_name("tblCouponEvents")
            for game_element in games:
                home, away = self._getBetslipHomeTeam(game_element)
                home = " ".join(home.split()[1:])
                prediction = self._getBetslipPrediction(game_element)
                market = self._getBetslipMarket(game_element)
                odds = self._getBetslipOdds(game_element)
                self._betslipGames.append([home, away, market, prediction, odds])

    def _getBetslipHomeTeam(self, webElement: WebElement) -> str:
        event_details = webElement.find_element_by_class_name("eventDetails")
        return event_details.find_elements_by_tag_name("div")[2].text.strip().split(" - ")

    def _getBetslipAwayTeam(self, webElement: WebElement) -> str:
        pass

    def _getBetslipPrediction(self, webElement: WebElement) -> str:
        mkt = webElement.find_element_by_class_name("currentOdds")
        return mkt.find_element_by_tag_name("div").find_element_by_tag_name("div").text.split()[-1]

    def _getBetslipOdds(self, webElement: WebElement) -> str:
        odds = webElement.find_element_by_class_name("currentOdds")
        odd_val = odds.find_element_by_class_name("oddValue")
        return odd_val.find_element_by_tag_name("div").text

    def _getBetslipMarket(self, webElement: WebElement) -> str:
        mkt = webElement.find_element_by_class_name("currentOdds")
        return mkt.find_element_by_tag_name("span").text