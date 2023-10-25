import os
import boto3
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


OLX_LINK = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bprivate_business%5D=private&search%5Border%5D=created_at:desc"

MAX_PRICE = os.environ.get("MAX_PRICE", 2700)
MIN_PRICE = os.environ.get("MAX_PRICE", 1500)
MIN_AREA = os.environ.get("MIN_AREA", 35)
PROHIBITED_DISTRICTS = ["Białołęka", "Ursus", "Wawer", "Targówek", "Bemowo"]


def get_html():
    options = Options()
    options.binary_location = "./headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("./chromedriver", options=options)
    driver.get(OLX_LINK)
    wait = WebDriverWait(driver, 20)
    element = EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler")
    )
    wait.until(element).click()
    return driver.page_source


def get_offers():
    result = []
    soup = BeautifulSoup(get_html(), "html.parser")
    offers = soup.find_all("div", {"class": "css-1sw7q4x"})
    for offer in offers:
        try:
            if offer.find_all("div", {"class": "css-1jh69qu"}):
                # WYRÓŻNIONE
                continue

            if not offer.find("span", {"class": "css-643j0o"}):
                # REKLAMA
                continue

            area_element = offer.find("span", {"class": "css-643j0o"})
            if not area_element or MIN_AREA > float(
                area_element.contents[1]
                .replace("m²", "")
                .replace(" ", "")
                .replace(",", ".")
            ):
                continue

            district = (
                offer.find("p", {"class": "css-veheph er34gjf0"})
                .contents[0]
                .split(" -")[0]
                .split(" ")[1]
            )
            if district in PROHIBITED_DISTRICTS:
                continue

            price = offer.find_all("p", {"class": "css-10b0gli er34gjf0"})[0].contents[
                0
            ]
            int_price = int(price.replace(" ", "").replace("zł", ""))
            if MIN_PRICE <= int_price <= MAX_PRICE:
                link = offer.next.get_attribute_list("href")[0]
                if link.startswith("/d"):
                    result.append("https://www.olx.pl" + link)
                else:
                    result.append(link)
        except Exception as err:
            print(">>>>>>>>>>>>>>>>>>>", err)
            continue
    return len(result), result


def get_offers_list_items(offers):
    result = ""
    for offer in offers:
        result += f"<li>{offer}</li><br/>"
    return result


def send_email(count, offers):
    client = boto3.client("ses")
    body_html = f"""<html>
        <head></head>
        <body>
          <h2>Nowe oferty!</h2>
          <br/>
          <p>Liczba ofert: {count}</p>
          {get_offers_list_items(offers)}
        </body>
        </html>
                    """

    email_message = {
        "Body": {
            "Html": {
                "Charset": "utf-8",
                "Data": body_html,
            },
        },
        "Subject": {
            "Charset": "utf-8",
            "Data": "Oferty z OLX",
        },
    }

    client.send_email(
        Destination={
            "ToAddresses": os.environ.get("TO_ADDRESSES", "").split(","),
        },
        Message=email_message,
        Source="k.gorzyn145@wp.pl",
        ConfigurationSetName="olx_raider_config_set",
    )


def lambda_handler(event, context):
    o_count, offers = get_offers()
    send_email(o_count, offers)
    sys.exit(0)
    # return {
    #     'statusCode': 200
    # }


lambda_handler("", "")
