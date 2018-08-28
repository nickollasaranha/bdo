from bs4 import BeautifulSoup
import urllib.request
import json

# edipo = urllib.request.open(ITEM_DEFAULT_URL.format(id, language))
# edipo.read
ITEM_DEFAULT_URL = "https://bddatabase.net/tip.php?id=item--{}&enchant=0&l={}&nf=on"
LANGUAGES = ["us", "pt"]
DEFAULT_T1_T3_PROC = 0.03
DEFAULT_PROCESSING_TIME = 8

# things to generate
itens_price = {}
itens_definition = {}
processing_itens = {}

with open("processing.html", encoding="utf8") as fp:
  soup = BeautifulSoup(fp, features="html.parser")

trs = soup.tbody("tr")

def get_item_profission(row_tds):
  return row_tds[5].string

def item_id_find(tag):
  return tag.has_attr('data-id') and tag.name == "a"

# This function will get the item name in all languages
def define_item(item_id):

  # We don't need to re-add itens
  if item_id in itens_definition: return

  languages = {}
  for lang in LANGUAGES:
    data = urllib.request.urlopen(ITEM_DEFAULT_URL.format(item_id, lang)).read()
    soup = BeautifulSoup(data, features="html.parser")
    item_name = soup.span.text
    languages[lang] = item_name

    if lang is "us":
      item_weight = float(soup("td")[2].prettify().split("Weight: ")[1].split(" LT")[0])

  itens_definition[item_id] = {"name": languages, "weight": item_weight}
  itens_price[item_id] = {"price": 0}

# This function will get the requirements of a given row
def get_item_requirements(row_tds):
  item_requirements = row_tds[6](item_id_find)
  requires = {}
  for item_required in item_requirements:
    try:
      item_id = int(item_required["data-id"].replace("item--", ""))
    except Exception:
      print(item_id)
      return {}
    try:
      item_qtd = int(item_required("div", class_="quantity_small nowrap")[0].text)
    except Exception:
      item_qtd = 1
    requires[item_id] = item_qtd
    define_item(item_id)

  return requires

# This function must return the item id and it's byproducts
def get_item_byproducts(row_tds):
  item_products = row_tds[7](item_id_find)
  # first item is the item itself
  byproducts = {}
  
  for i in range(len(item_products)):
    item_aux_id = int(item_products[i]["data-id"].replace("item--", ""))
    define_item(item_aux_id)

    if i == 0:
      item_id = item_aux_id
      continue

    byproducts[item_id] = DEFAULT_T1_T3_PROC

  return item_id, byproducts

for row in trs:
  tds = row("td")
  processing_dict = {}
  item_id, item_byproducts = get_item_byproducts(tds)
  processing_dict["profission"] = get_item_profission(tds)
  processing_dict["time_required"] = DEFAULT_PROCESSING_TIME
  processing_dict["requirements"] = get_item_requirements(tds)
  processing_dict["byproducts"] = item_byproducts
  processing_itens[item_id] = processing_dict.copy()

with open('itens_definition.json', 'w') as f:
  json.dump(itens_definition, f, indent=4, ensure_ascii=False)

with open('processing_itens.json', 'w') as f:
  json.dump(processing_itens, f, indent=4, ensure_ascii=False)

with open('itens_price.json', 'w') as f:
  json.dump(itens_price, f, indent=4, ensure_ascii=False)