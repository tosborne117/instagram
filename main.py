#from operator import truediv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

username = 'user'
password = 'password'

#takes user input, and enters it as username and password for Instagram login
def login(driver):
    #user input
    global username
    global password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    #Instragram login through webdriver
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    loginButton = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]')
    loginButton.click()

    return username

#extracts and returns user followers
def findFollowers(driver):
    #access user account
    global username
    profilePage = '[alt*="' + username + '"]'
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, profilePage)))
    element.click()
    #access followers
    followers = '[href*="' + username + '/followers/''"]'
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, followers)))
    element.click()

    #pull data
    list_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[4]"
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, list_xpath)))

    #scroll down
    #scroll_limit = (int)(followerCount / 18)
    scroll_limit = 20
    for _ in range(scroll_limit):
        time.sleep(2)
        scroll = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[4]")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)

    list_elements = driver.find_elements(By.CLASS_NAME, "x9f619")
    time.sleep(1)
    print(len(list_elements))

    followersList = []
    for i in range(len(list_elements)):
        try:
            row_text = list_elements[i].text
            if 'Remove' in row_text:
                follower = row_text[:row_text.index("\n")]
                followersList += [follower]
        except:
            print('continue')

    # close followers tab
    close = '[aria-label="Close"]'
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, close)))
    element.click()

    followersDF = pd.DataFrame(followersList)
    followersDF.drop_duplicates(keep='first', inplace=True)
    return followersDF

#extracts and returns users following
def findFollowing(driver):
    #access following
    global username
    following = '[href*="' + username + '/following/''"]'
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, following)))
    element.click()

    #pull data
    list_xpath = "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[4]"
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, list_xpath)))

    # scroll down
    scroll_limit = 20
    for _ in range(scroll_limit):
        time.sleep(2)
        scroll = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[4]")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)

    list_elements = driver.find_elements(By.CLASS_NAME, "x9f619")
    time.sleep(1)

    followingList = []
    for i in range(len(list_elements)):
        try:
            row_text = list_elements[i].text
            if 'Following' in row_text:
                following = row_text[:row_text.index("\n")]
                followingList += [following]
        except:
            print('continue')

    #close following tab
    close = '[aria-label="Close"]'
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, close)))
    element.click()

    followingDF = pd.DataFrame(followingList)
    followingDF.drop_duplicates(keep='first', inplace=True)
    return followingDF

def check_difference_in_count(driver):
    global count
    new_count = len(driver.find_elements(By.XPATH, "//div[@role='dialog']//li"))
    if count != new_count:
        count = new_count
        return True
    else:
        return False

def __main__():
    #instantiate webdriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.instagram.com/accounts/login/?hl=en')
    time.sleep(1)

    #login
    name = login(driver)
    #generate list of followers
    followersList = findFollowers(driver)
    print(followersList)
    #followersList.sort_values(by=['followers'])
    #generate list of following
    followingList = findFollowing(driver)
    #followingList.sort_values(by=['following'])

    #compare list
    followingList.rename(columns={0: 'Following'}, inplace=True)
    followersList.rename(columns={0: 'Followers'}, inplace=True)
    followingDF = followingList.tail(-1)
    followerDF = followersList.tail(-1)

    print(followingDF, '\n', followerDF)

    notFollowingBack = []
    for i, name in followingDF['Following'].items():
        if name in followerDF['Followers'].values:
            continue
        else:
            notFollowingBack.append(name)

    print(notFollowingBack)
    time.sleep(1000)
    return

__main__()


