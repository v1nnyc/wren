from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import smtplib, ssl

port = 465  # For SSL

# method to webscrabe humane society to see if wren has been put up for adoption
def isWrenAvailable():
    # TODO replace with wrens ID
    pet_id_to_search = 228652

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(
        "https://www.sdhumane.org/adopt/available-pets/?petType=ALL&physicalLocationId=ALL&genderSearch=All&searchAge=All&searchName=&searchId={}".format(
            pet_id_to_search
        )
    )
    delay = 3
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "petId")))
    except TimeoutException:
        return False

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for div in soup.findAll("span", {"class": "petId"}):
        if div.next_element == " #{}".format(pet_id_to_search):
            return True


def emailMe():
    print("emailing.. lol")
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl.create_default_context()) as server:
        server.login("vcannall@gmail.com", "vtslgyxfmzqqewvq")
        server.sendmail("vcannall@gmail.com", "vcannall@gmail.com", "WREN IS AVAILABLE")


# main
while True:
    if isWrenAvailable():
        emailMe()
