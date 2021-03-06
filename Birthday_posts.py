from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from sys import exit
from os.path import expanduser

Messages = []
random.seed()

headers = {'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'max-age=0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
}


def Facebook_Login():
    global headers

    # Identifies which browswer is being used
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS(desired_capabilities=headers)
    #driver.set_window_size(1366, 768)

    # uses the login website and logs into facebook
    driver.get('https://www.facebook.com/login')

    location = expanduser('~/.facebook')
    account = open(location, 'r')
    login = account.readline().strip('\n')
    passwd = account.readline().strip('\n')
    account.close()
    username = driver.find_element_by_id('email')
    password = driver.find_element_by_id('pass')

    username.send_keys(login)
    password.send_keys(passwd)

    driver.find_element_by_id('loginbutton').click()

    return driver


def GetMessageList():
    global Messages
    msg = open("Birthday Messages.txt", 'r')
    Messages.extend(msg.read().strip('\n').splitlines())


def GetRandomMessage():
    global Messages
    return Messages[random.randint(0, len(Messages)-1)]
    
    
def Post_Messages(driver):
    sleep(4)
    driver.get("https://m.facebook.com/birthdays/")

    # If there are birthdays today, then it will continue, otherwise, it will exit
    try:
        notification = driver.find_element_by_xpath("//*[contains(text(), 'Today')]")
        print "Notifications are " + str(notification)

    except:
        print "There are no birthdays going on today \n\n"
        driver.save_screenshot('screenshot.png')
        exit()

    # Gets the names of the birthday people
    Birthday_names = driver.find_elements_by_xpath('//*[@id="events_card_list"]/article[1]/div/div/ul/div/a/div/p[1]')

    # Keeps track of people who have passed away, but still have active accounts
    fptr = open("Passed_Away.txt")
    Passed = fptr.read().strip('\n').splitlines()
    fptr.close()

    # Identifies any of the people who passed away have birthdays today
    indexes = [i for i, x in enumerate(Birthday_names) if x in Passed]
    
    # Sends a birthday post for every user that has there birthday today
    for i in range(1, len(Birthday_names)+1):
        # If they passed away, avoid giving them a birthday note
        if (i-1 in indexes):
            continue
        formpath = '//*[@id="events_card_list"]/article[1]/div/div/ul/div[%d]/div/div/form/table/tbody/tr/td[1]/textarea' %i
        driver.find_element_by_xpath(formpath).send_keys(GetRandomMessage() + Keys.TAB + Keys.ENTER)


try:
    GetMessageList()
    driver = Facebook_Login()
    Post_Messages(driver)
    driver.close()


except Exception, e:
    driver.save_screenshot('screenshot.png')
    driver.close()
    print "Error happened " + str(e.message)
