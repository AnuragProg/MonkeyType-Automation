import os
from time import sleep
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
        '''
        Initializes chrome_driver with basic settings
        '''
        service = Service(self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_driver = webdriver.Chrome(service=service, options=options)
        self.chrome_driver.set_window_position(-1,0)
        self.chrome_driver.set_window_size(790,800)
    
    def open_main_website(self):
        f'''
        Opens main website at {self.WEBSITEURL}
        '''
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
        '''
        Opens given url in the browser
        '''
        self.chrome_driver.get(url)
    
    def refresh(self):
        '''
        Refreshes Browser
        '''
        self.chrome_driver.refresh()
    
    def close_browser(self):
        '''
        Closes Browser
        '''
        self.chrome_driver.quit()

    def check_for_cookie_message_box(self):
        '''
        Closes any cookie message box by accepting the cookies
        '''
        try:
            cookie_button = self.chrome_driver.find_element(By.XPATH, "//div[.='Accept all']")
            cookie_button.click()
        except NoSuchElementException as exception:
            pass
        except ElementNotInteractableException as exception:
            pass

    def check_and_handle_out_of_focus_warning(self):
        '''
        Currently of no use
        '''
        try:
            self.chrome_driver.find_element(By.CLASS_NAME, "outOfFocusWarning")
            self.chrome_driver.find_element(By.ID, "wordsInput").click()

        except NoSuchElementException as exception:
            print(exception)
        finally:
            print("OutOfFocusWarning Handled Successfully")
    

    def set_time_option(self, time: int = 60, punctuation: bool = False, numbers: bool = False):
        '''
        Sets up the page for 'Time' mode play
        '''

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
        time_button.click()

        # wait and click for time mode
        WebDriverWait(self.chrome_driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, clickable_time[time])
            )
        )
        sleep(2)
        amount_of_time_button = self.chrome_driver.find_element(By.XPATH, clickable_time[time])
        amount_of_time_button.click()

        # check punctuation option
        if punctuation:
            sleep(1)
            punctuation_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='punctuation']")
            punctuation_toggle_button.click()
            print("Clicked Punctuation")

        # check numbers option
        if numbers:
            sleep(1)
            numbers_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='numbers']")
            numbers_toggle_button.click()
            print("Clicked Numbers")

    
    def set_words_option(self, no_of_words: int = 50, punctuation: bool = False, numbers: bool = False):
        '''
        Sets up the page for 'Word' mode play
        '''
        clickable_word_count = {
            10: "//div[contains(@class, 'textButton') and @wordcount='10']",
            25: "//div[contains(@class, 'textButton') and @wordcount='25']",
            50: "//div[contains(@class, 'textButton') and @wordcount='50']",
            100: "//div[contains(@class, 'textButton') and @wordcount='100']"
        }

        # if no_of_words is not in clickables
        if no_of_words not in clickable_word_count.keys():
            raise ValueError
        
        # makes the typing test based on 'words'
        words_mode_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton') and @mode='words']")
        words_mode_button.click()
    

        # wait and click for words mode
        WebDriverWait(self.chrome_driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, clickable_word_count[no_of_words])
            )
        )
        sleep(2)
        amount_of_words_button = self.chrome_driver.find_element(By.XPATH, clickable_word_count[no_of_words])
        amount_of_words_button.click()
        


        # check punctuation option
        if punctuation:
            sleep(1)
            punctuation_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='punctuation']")
            self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton toggleButton active')", punctuation_toggle_button)
            print("Clicked Punctuation")

        # check numbers option
        if numbers:
            sleep(1)
            numbers_toggle_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton toggleButton') and text()='numbers']")
            self.chrome_driver.execute_script("arguments[0].setAttribute('class', 'textButton toggleButton active')", numbers_toggle_button)
            print("Clicked Numbers")
    

    def set_quote_option(self, choice: str):
        '''
        Sets up the page for 'Quote' mode play
        '''
        clickable_choice = {
            'all': "//div[contains(@class, 'textButton') and text()='all']",
            'short': "//div[contains(@class, 'textButton') and text()='short']", 
            'medium': "//div[contains(@class, 'textButton') and text()='medium']", 
            'long': "//div[contains(@class, 'textButton') and text()='long']", 
            'thicc': "//div[contains(@class, 'textButton') and text()='thicc']"
        }

        # if choice is not in clickables
        if choice not in clickable_choice.keys():
            raise ValueError
        
        # makes the typing test based on 'quote'
        quotes_button = self.chrome_driver.find_element(By.XPATH, "//div[contains(@class,'textButton') and @mode='quote']")
        quotes_button.click()

        
        # wait and click for quote mode
        WebDriverWait(self.chrome_driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, clickable_choice[choice])
            )
        )
        sleep(2)
        amount_of_quotes_button = self.chrome_driver.find_element(By.XPATH, clickable_choice[choice])
        amount_of_quotes_button.click()


    def fetch_word_and_send_keys(self):
        '''
        Fetches the current active word and sends the respective keys
        '''
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
        3: 'quote',
        4: "[Quit]"
    }
    monkeyType = MonkeyType()
    monkeyType.open_main_website()
    
    while True:
        monkeyType.check_for_cookie_message_box()
        for id in options.keys():
            print("%d. - %s"%(id, options[id]))
        try:
            user_selected_option = int(input("Your choice -> "))
            if user_selected_option not in options.keys():
                raise ValueError
            if user_selected_option == 4:
                print("Good Bye!")
                monkeyType.close_browser()
                exit()
        except ValueError:
            os.system('cls')
            print("Please Enter Valid Option")
            continue
        user_selected_option = options[user_selected_option]

        # Play monkeytype in time mode
        if user_selected_option == 'time':
            time_options = {
                1: 15,
                2: 30,
                3: 60,
                4: 120,
                5: "[Back To Main Menu]"
            }
            print("Select Time: ")
            for time in time_options.keys():
                print(f"{time} - {time_options[time]} sec")
            try:
                user_selected_option = int(input("Your choice -> "))
                if user_selected_option not in time_options.keys():
                    raise ValueError
                if user_selected_option == 5:
                    os.system('cls')
                    continue
            except ValueError:
                os.system('cls')
                print("Please Enter Valid Option")
                continue

            user_selected_time = time_options[user_selected_option]
            want_punctuation = False
            want_numbers = False
            print("Do you want to select 'Punctuation'? (y)es or (n)o")
            user_selected_option = input("Your response -> ")
            user_selected_option.strip()
            if user_selected_option.lower() == 'y' or user_selected_option.lower() == 'yes':
                want_punctuation = True
            
            print("Do you want to select 'Numbers'? (y)es or (n)o")
            user_selected_option = input("Your response -> ")
            user_selected_option.strip()
            if user_selected_option.lower() == 'y' or user_selected_option.lower() == 'yes':
                want_numbers = True
            
            monkeyType.set_time_option(time = user_selected_time, punctuation = want_punctuation, numbers = want_numbers)
            monkeyType.fetch_word_and_send_keys()

        # Play monkeytype in words mode
        elif user_selected_option == 'words':
            word_options = {
                1: 10,
                2: 25,
                3: 50,
                4: 100,
                5: "[Back To Main Menu]"
            }
            print("Select Words: ")
            for word in word_options.keys():
                print(f"{word} - {word_options[word]} words")
            try:
                user_selected_option = int(input("Your choice -> "))
                if user_selected_option not in word_options.keys():
                    raise ValueError
                if user_selected_option == 5:
                    os.system('cls')
                    continue
            except ValueError:
                os.system('cls')
                print("Please Enter Valid Option")
                continue

            user_selected_words = word_options[user_selected_option]
            want_punctuation = False
            want_numbers = False
            print("Do you want to select 'Punctuation'? (y)es or (n)o")
            user_selected_option = input("Your response -> ").strip().lower()
            if user_selected_option == 'y' or user_selected_option == 'yes':
                want_punctuation = True
            
            print("Do you want to select 'Numbers'? (y)es or (n)o")
            user_selected_option = input("Your response -> ").strip().lower()
            if user_selected_option == 'y' or user_selected_option == 'yes':
                want_numbers = True
            
            monkeyType.set_words_option(no_of_words = user_selected_words, punctuation = want_punctuation, numbers = want_numbers)
            monkeyType.fetch_word_and_send_keys()

        # Play monkeytype in quote mode
        elif user_selected_option == 'quote':
            quote_options = {
                1: 'all',
                2: 'short',
                3: 'medium',
                4: 'long',
                5: 'thicc',
                6: '[Back To Main Menu]'
            }
            print("Select Quote: ")

            for quote in quote_options.keys():
                print(f"{quote} - {quote_options[quote]}")
            try:
                user_selected_option = int(input("Your choice -> "))
                if user_selected_option not in quote_options.keys():
                    raise ValueError
                if user_selected_option == 6:
                    os.system('cls')
                    continue
            except ValueError:
                os.system('cls')
                print("Please Enter Valid Option")
                continue
            
            user_selected_choice = quote_options[user_selected_option]
            
            monkeyType.set_quote_option(user_selected_choice)
            monkeyType.fetch_word_and_send_keys()
        
        print("Do you want to (c)ontinue or (q)uit?")
        user_selected_option = input("Your choice -> ").strip().lower()

        if user_selected_option == 'c' or user_selected_option == 'continue':
            monkeyType.refresh()
            os.system('cls')
        else: 
            print("Good Bye!")
            monkeyType.close_browser()
            exit()