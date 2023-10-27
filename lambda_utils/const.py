import os

# general
IS_LOCAL = os.environ.get("IS_LOCAL", "False") == "True"
OLX_LINK = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bprivate_business%5D=private&search%5Border%5D=created_at:desc"
MAX_PRICE = os.environ.get("MAX_PRICE", 2700)
MIN_PRICE = os.environ.get("MAX_PRICE", 1500)
MIN_AREA = os.environ.get("MIN_AREA", 35)
PROHIBITED_DISTRICTS = ["Białołęka", "Ursus", "Wawer", "Targówek", "Bemowo"]

# bs
OFFERS_CLASS_NAME = "css-1sw7q4x"
AWARDED_CLASS_NAME = "css-1jh69qu"
AREA_CLASS_NAME = "css-643j0o"
OFFER_CLASS_NAME = "css-veheph er34gjf0"
PRICE_CLASS_NAME = "css-10b0gli er34gjf0"

# mail
SOURCE_EMAIL = os.environ.get("SOURCE_EMAIL")
