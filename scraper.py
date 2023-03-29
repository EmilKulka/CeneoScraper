import requests
from bs4 import BeautifulSoup

# product_code = input("Podaj kod produktu: ")
product_code = "123849599"
# url = "https://www.ceneo.pl/"+ product_code +"#tab=reviews"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")
opinions = page_dom.select("div.js_product-review")
for opinion in opinions:
    print(opinion["data-entry-id"])
