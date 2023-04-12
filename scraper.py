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
selectors = {
        "opinion_id": [ None, "data-entry-id"],
        "author": ["span.user-post__author-name"],
        "recommendation": ["span.user-post__author-recomendation > em"],
        "stars": ["span.user-post__score-count"],
        "purchased": ["div.review-pz"],
        "opinion_date": ["span.user-post__published > time:nth-child(1)","datetime"],
        "purchase_date": ["span.user-post__published > time:nth-child(2)","datetime"],
        "useful": ["button.vote-yes > span"],
        "unuseful": ["button.vote-no > span"],
        "content": ["div.user-post__text"],
        "cons": ["div.review-feature__col:has(> div.review-feature__item", None, True],
        "pros": ["div.review-feature__col:has(> div.review-feature__item", None, True]
    }
# product_code = input("Podaj kod produktu: ")
product_code = "123849599"
# url = "https://www.ceneo.pl/"+ product_code +"#tab=reviews"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")
opinions = page_dom.select("div.js_product-review")
all_opinions = []
for opinion in opinions:
    single_opinion = {}
    for key, value in selectors.items():
        single_opinion[key] = get_element(opinion, *value)
    all_opinions.append(single_opinion)

with open(f"./opinions/{product_code}.json", "w", encoding= "UTF-8") as jf:
    json.dump(all_opinions,jf, indent = 4, ensure_ascii = False)
print(json.dumps(all_opinions, indent = 4, ensure_ascii = False))
