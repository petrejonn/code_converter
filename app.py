# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# chrome_options = Options()
# # chrome_options.add_argument("--disable-extensions")
# # chrome_options.add_argument("--disable-gpu")
# # chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(options=chrome_options)
# action = ActionChains(driver)

# start_url = "https://web.bet9ja.com/Sport/Default.aspx"
# driver.get(start_url)


# from slip_converter import scraper

# print("============ Bet9ja Started ===================")
# scraper.scrapeBet9ja()
# print("============ SportyBet Started ===================")
# scraper.scrapeSportybet()
# print("============ BetKing Started ===================")
# scraper.scrapeBetking()

from slip_converter.bookmakers.betking import Betking
from slip_converter.bookmakers.bet9ja import Bet9ja
# games = ((('Basel','Krasnodar'), '1x2', 'Draw'),)
# inst = BetkingBookMaker()
# inst.bookGames(games)
# print(inst.getBookingCode())
# print(inst.getBookingGames())
# print(BetkingBookMaker.loadCode("D9FJZ"))

from slip_converter.converter import CodeConverter

ins = CodeConverter("ZBH75GZ", Bet9ja(), Betking())
ins.convert()
print(ins.getNewCode())