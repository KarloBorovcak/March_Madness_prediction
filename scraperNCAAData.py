from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


year = 2013
stats_type = ["-opponent-stats", "-advanced-school-stats", "-advanced-opponent-stats"]
page = "https://www.sports-reference.com/cbb/seasons/" + str(year) + "-school-stats.html"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
ser = Service("C:\Program Files (x86)\chromedriver.exe")
driver = webdriver.Chrome(service=ser)

driver.get(page)
driver.find_element(By.CLASS_NAME, 'css-47sehv').click()
a = ActionChains(driver)

def store_data(data, filename):
    with open('./data/'+ filename + '.csv', 'w') as out:
        out.write(data)
    

def find_data(driver, a, filename):
    driver.execute_script("window.scrollTo(0, 500)") 
    sleep(3)
    div = driver.find_element(By.CLASS_NAME,"sidescroll_note")
    ul = div.find_element(By.TAG_NAME,'ul')
    menu = ul.find_element(By.CLASS_NAME,'hasmore')
    a.move_to_element(menu).click().perform()

    options = driver.find_elements(By.CLASS_NAME, 'tooltip')
    options[2].click()


    # uzmi podatke
    sleep(2)
    parent = driver.find_element(By.CSS_SELECTOR, 'div[style="overflow:auto"]')
    data = parent.find_element(By.TAG_NAME,'pre')
    
    index = data.text.find(',', data.text.find(',')+1)
    data = data.text[index:]
    
    store_data(data, filename)

while year < 2023:

    find_data(driver, a, str(year) + "-school-stats")

    for stat in stats_type:
        page = "https://www.sports-reference.com/cbb/seasons/" + str(year) + stat + ".html"
        driver.get(page)
        find_data(driver, a, str(year) + stat)

    year += 1
    page = "https://www.sports-reference.com/cbb/seasons/" + str(year) + "-school-stats.html"
    driver.get(page)




