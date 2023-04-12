import requests
import json
from bs4 import BeautifulSoup

def get_element(ancestor, selector=None, attributte = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)]
        if not selector and attributte:
            return ancestor[attributte]
        if attributte:
            return ancestor.select_one(selector)[attributte].strip()
        return ancestor.opinion.select_one(selector).text.strip()
    except (AttributeError,TypeError):
        return None
# product_code = input("Podaj kod produktu: ")
product_code = "123849599"
# url = "https://www.ceneo.pl/"+ product_code +"#tab=reviews"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")
opinions = page_dom.select("div.js_product-review")
all_opinions = []
for opinion in opinions:
    single_opinion = {
        "opinion_id": get_element(opinion, None, "data-entry-id"),
        "author": get_element(opinion, "span.user-post__author-name"),
        "recommendation": get_element(opinion,"span.user-post__author-recomendation > em"),
        "stars": get_element(opinion,"span.user-post__score-count"),
        "purchased": get_element(opinion,"div.review-pz"),
        "opinion_date": get_element(opinion,"span.user-post__published > time:nth-child(1)", "datetime"),
        "purchase_date": get_element(opinion,"span.user-post__published > time:nth-child(2)", "datetime"),
        "useful": get_element(opinion,"button.vote-yes > span"),
        "unuseful": get_element(opinion,"button.vote-no > span"),
        "content": get_element(opinion,"div.user-post__text"),
        "cons": get_element(opinion,"div.review-feature_title--negatives ~ div.review-feature__item", None, True),
        "pros": get_element(opinion,"div.review-feature_title--positives ~ div.review-feature__item", None, True),
    }
    all_opinions.append(single_opinion)

with open(f"./opinions/{product_code}.json", "w", encoding= "UTF-8") as jf:
    json.dump(all_opinions,jf, indent = 4, ensure_ascii = False)
print(json.dumps(all_opinions, indent = 4, ensure_ascii = False))
