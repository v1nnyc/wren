from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

import smtplib
import ssl

from datetime import datetime

# pet_id_to_search = 633418
pet_id_to_search = 21714  # used for testing an available pet

# selenium config
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


# method to webscrabe humane society to see if wren has been put up for adoption
def isWrenAvailable():
    driver.get(
        "https://www.sdhumane.org/adopt/available-pets/?petType=ALL&physicalLocationId=ALL&genderSearch=All&searchAge=All&searchName=&searchId={}".format(
            pet_id_to_search
        )
    )
    delay = 3
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "petId")))
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        for div in soup.findAll("span", {"class": "petId"}):
            if div.next_element == " #{}".format(pet_id_to_search):
                driver.stop_client()
                driver.close()
                return True
    except TimeoutException:
        return False


def emailMe():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login("vcannall@gmail.com", "vtslgyxfmzqqewvq")
        server.sendmail(
            "vcannall@gmail.com",
            "vcannall@gmail.com",
            """
            https://www.sdhumane.org/adopt/available-pets/?petType=ALL&physicalLocationId=ALL&genderSearch=All&searchAge=All&searchName=&searchId={}
            """.format(
                pet_id_to_search
            ),
        )


# main
i = 1
while 1 > 0:
    print(datetime.now(), i)
    i += 1
    if isWrenAvailable():
        print("Wren was made available at {}".format(datetime.now()))
        emailMe()
        break
