'''
time = [15,30,60,120] -> extras (can be both selected) [punctuation, numbers]
words = [10,25,50,100] -> extras (can be both selected) [punctuation, numbers]
quote = [all, short, medium, long, thicc]
'''
import os
from time import sleep
from turtle import clear
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By

class MonkeyType:

    WEBSITEURL = "https://monkeytype.com/"
    chrome_driver_path = "chromedriver.exe"
    chrome_driver = None

    def __init__(self):
        service = Service(self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_driver = webdriver.Chrome(service=service, options=options)
    
    def open_main_website(self):
        print("Opening %s"%(self.WEBSITEURL))
        self.__open_website(self.WEBSITEURL)
        try:
            WebDriverWait(self.chrome_driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR, "div[class='word active']"
                    )
                )
            )
        except TimeoutException as exception:
            print("Unable to load website")
            exit()

    def __open_website(self, url: str):
        self.chrome_driver.get(url)
    
    def refresh(self):
        self.chrome_driver.refresh()

    def check_for_cookie_message_box(self):
        try:
            cookie_button = self.chrome_driver.find_element(By.XPATH, "//div[.='Accept all']")
            cookie_button.click()
        except NoSuchElementException as exception:
            pass
        except ElementNotInteractableException as exception:
            pass

    def check_and_handle_out_of_focus_warning(self):
        try:
            self.chrome_driver.find_element(By.CLASS_NAME, "outOfFocusWarning")
            self.chrome_driver.find_element(By.ID, "wordsInput").click()

        except NoSuchElementException as exception:
            print(exception)
        finally:
            print("OutOfFocusWarning Handled Successfully")
    

    def set_time_option(self, time: int = 60, punctuation: bool = False, numbers: bool = False):
        
        # different time buttons and their respective xpath
        clickable_time = {
            15: "//div[contains(@class,'textButton') and @timeconfig='15'] ",
            30: "//div[contains(@class, 'textButton') and @timeconfig='30']",
            60: "//div[contains(@class, 'textButton') and @timeconfig='60']",
            120: "//div[contains(@class, 'textButton') and @timeconfig='120']"
        }

        # if time is not in clickables
        if time not in clickable_time.keys():
            raise ValueError
        
        # makes the typing test based on 'time'
        time_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class, 'textButton') and @mode='time']")
        self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton active')", time_button)

        # selecting user specified time
        self.chrome_driver.find_element(By.XPATH, clickable_time[time]).click()

        # check punctuation option
        if punctuation:
            punctuation_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='punctuation']")
            self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton toggleButton active')", punctuation_toggle_button)
            print("Clicked Punctuation")

        # check numbers option
        if numbers:
            numbers_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='numbers']")
            self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton toggleButton active')", numbers_toggle_button)
            print("Clicked Numbers")

    
    def set_words_option(self, no_of_words: int = 50, punctuation: bool = False, numbers: bool = False):
        clickable_word_count = [10, 25, 50, 100]

        # if no_of_words is not in clickables
        if no_of_words not in clickable_word_count:
            raise ValueError
        
        words_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton') and @mode='words']")
        self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton active')", words_button)
    
    def set_quote_option(self, choice: str):
        clickable_choice = ['all', 'short', 'medium', 'long', 'thicc']

        # if choice is not in clickables
        if choice not in clickable_choice:
            raise ValueError

    def fetch_word_and_send_keys(self):
        while True:
            try:
                active_word = self.chrome_driver.find_element(By.CSS_SELECTOR, "div[class='word active']")
                letters_of_active_word = active_word.find_elements(By.TAG_NAME, "letter")
                letters = [l.text for l in letters_of_active_word]
                print("Sending %s"%("".join(letters)))
                self.chrome_driver.find_element(By.ID, "wordsInput").send_keys("".join(letters) + " ")
                
                
            except NoSuchElementException as exception:
                break

            except ElementNotInteractableException as exception:
                break

            except StaleElementReferenceException as exception:
                pass
        print("All words sent Successfully")

if __name__ == '__main__':
    options = {
        1: 'time',
        2: 'words',
        3: 'quote'
    }
    monkeyType = MonkeyType()
    monkeyType.open_main_website()
    
    while True:
        # for id in options.keys():
        #     print("%d. - %s"%(id, options[id]))
        # try:
        #     user_selected_option = int(input())
        #     if user_selected_option not in options.keys():
        #         raise ValueError
        # except ValueError:
        #     os.system('cls')
        #     print("Please Enter Valid Option")
        #     continue
        # user_selected_option = options[user_selected_option]
        monkeyType.check_for_cookie_message_box()
        print("Cookie box closed")
        monkeyType.set_time_option(punctuation=True, numbers=True)
        monkeyType.fetch_word_and_send_keys()
        monkeyType.refresh()
        break
