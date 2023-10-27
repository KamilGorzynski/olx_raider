from bs4 import BeautifulSoup
from lambda_utils.selenium_utils import get_selenium_driver, get_html
from lambda_utils import const


def get_offers():
    result = []
    driver = get_selenium_driver()
    soup = BeautifulSoup(get_html(driver), "html.parser")
    driver.close()
    offers = soup.find_all("div", {"class": const.OFFERS_CLASS_NAME})
    for offer in offers:
        try:
            if offer.find_all("div", {"class": const.AWARDED_CLASS_NAME}):
                # WYRÓŻNIONE
                continue

            if not offer.find("span", {"class": const.AREA_CLASS_NAME}):
                # REKLAMA
                continue

            area_element = offer.find("span", {"class": const.AREA_CLASS_NAME})
            if not area_element or const.MIN_AREA > float(
                area_element.text.replace("m²", "").replace(" ", "").replace(",", ".")
            ):
                continue
            district = offer.find("p", {"class": const.OFFER_CLASS_NAME}).text.split(
                " "
            )[1]
            if district in const.PROHIBITED_DISTRICTS:
                continue
            price = "".join(
                filter(
                    str.isdigit, offer.find("p", {"class": const.PRICE_CLASS_NAME}).text
                )
            )
            int_price = int(price.replace(" ", "").replace("zł", ""))
            if const.MIN_PRICE <= int_price <= const.MAX_PRICE:
                link = offer.next.get_attribute_list("href")[0]
                if link.startswith("/d"):
                    result.append("https://www.olx.pl" + link)
                else:
                    result.append(link)
        except Exception as err:
            print(">>>>>>>>>>>>>>>>>>>", err)
            continue
    return len(result), result
