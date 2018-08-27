from bs4 import BeautifulSoup
import urllib.request

# edipo = urllib.request.open(ITEM_DEFAULT_URL.format(id, language))
# edipo.read
ITEM_DEFAULT_URL = "https://bddatabase.net/tip.php?id={}&enchant=0&l={}&nf=on"
LANGUAGES = ["us", "pt"]

# things to generate
itens = {}
processing_itens = {}

with open("processing.html", encoding="utf8") as fp:
  soup = BeautifulSoup(fp, features="html.parser")

trs = soup.tbody.find_all("tr")

def get_recipe_id(row_tds):
  return tds[0].string

def get_item_name(row_tds):
  return tds[2].string

def get_item_profission(row_tds):
  return tds[5].string

def get_item_requirements(row_tds):
  item_requirements = tds[6](item_id)
  item_ids = []
  for item_required in item_requirements:
    item_id = item_required["data-id"]
    item_qtd = item_required("div", class_="quantity small nowrap")[0].text
    print(item_required)

def get_item_byproducts(row_tds):
  item_products = tds[7]

for row in trs:
  tds = row.find_all("td")
  recipe_id = get_recipe_id(tds)
  item_name = get_item_name(tds)
  item_profission = get_item_profission(tds)
  item_requirements = get_item_requirements(tds)
  break

def item_id(tag):
  return tag.has_attr('data-id') and tag.name == "a"
#print (soup.tbody)
# def edipo(tag):
#   return tag.has_attr('colspan') and tag.name == "td" and tag.string == "ID: 1"

# soup = BeautifulSoup(html_page, features="html.parser")

# tbody_tag = soup.find_all(edipo)[0].parent.parent
# trs = tbody_tag.find_all("tr")

# # Set vars
# item = {}
# item["name"] = trs[1].string.lower()
# item["profission"] = trs[3].find_all('td')[1].find_all('span')[1].string.lower()
# item["requirements"] = {}


