from bs4 import BeautifulSoup
from progress.bar import Bar
import urllib.request
import threading
import json

# Change those vars if you wish
MAXIMUM_THREADS = 12
LANGUAGES = ["us", "pt"]
CRAFTING_FILE = "crafting.html"
PROCESSING_FILE = "processing.html"
DEFAULT_T1_T3_PROC = 0.03
DEFAULT_PROCESSING_TIME = 8
DEFAULT_COOK_PROCESSING_TIME = 3
DEFAULT_ALCHEMY_PROCESSING_TIME = 5
DEFAULT_PROC_PER_PROCESS = 2.5

# Don't change vars below
ITEM_DEFAULT_URL = "https://bddatabase.net/tip.php?id=item--{}&enchant=0&l={}&nf=on"
GROUP_DEFAULT_URL = "https://bddatabase.net/tip.php?id=materialgroup--{}&enchant=0&l={}&nf=on"

# Things to generate
itens_group_definition = {}
aux_recipes = {}
crafting_itens = {}
itens_definition = {}
itens_group_cv = threading.Condition(threading.Lock())
itens_definition_cv = threading.Condition(threading.Lock())
aux_recipes_cv = threading.Condition(threading.Lock())
crafting_itens_cv = threading.Condition(threading.Lock())

threadLimiter = threading.BoundedSemaphore(MAXIMUM_THREADS)

def load_item_definition():
  try:
    with open("itens_definition.json", encoding="utf8", mode="r") as f:
      itens_definition = json.load(f)
  except Exception as err:
    print ("Failed to load itens_definition. It will be re-defined.")
    print (err)

# This function returns the recipe id
def get_recipe_id(row_tds):
  return row_tds[0].string

# This function returns the Profission of a row
def get_item_profission(row_tds):
  return row_tds[5].string

# This function is used to perform a search for data-id
def item_id_find(tag):
  return tag.has_attr('data-id') and tag.name == "a"

# This function will get the item name in all languages
def define_item(item_id, tipo):

  # We can have tipo == "item" or "group"
  if tipo == "group":
    itens_group = set()

    # Don't readd groups
    if item_id in itens_group_definition: return

    # Request URL
    data = urllib.request.urlopen(GROUP_DEFAULT_URL.format(item_id, "us")).read()
    soup = BeautifulSoup(data, features="html.parser")
    group_name = soup("tr")[1].text.strip().split("Item group")[0]

    # Get all itens in the group
    for item_aux_id in soup("tr")[2](item_id_find):
      item_id_aux = int(item_aux_id["data-id"].replace("item--", ""))
      itens_group.add(item_id_aux)
      define_item(item_id_aux, "item")

    # Populate group definition
    itens_group_cv.acquire()
    itens_group_definition[item_id] = {"name": group_name, "itens": list(itens_group)}
    itens_group_cv.release()
    return

  # IF tipo == "item"
  # We don't need to re-add itens
  if item_id in itens_definition: return

  languages = {}
  for lang in LANGUAGES:
    data = urllib.request.urlopen(ITEM_DEFAULT_URL.format(item_id, lang)).read()
    soup = BeautifulSoup(data, features="html.parser")
    item_name = soup("tr")[1].text.strip()
    languages[lang] = item_name

    if lang is "us":
      item_weight = float(soup("td")[2].prettify().split("Weight: ")[1].split(" LT")[0])

  # Populate itens definition
  itens_definition_cv.acquire()
  itens_definition[item_id] = {"name": languages, "weight": item_weight, "price": -1}
  itens_definition_cv.release()

# This function will get the requirements of a given row
def get_item_requirements(row_tds):
  item_requirements = row_tds[6](item_id_find)
  item_requires = {}
  group_requires = {}

  for item_required in item_requirements:

    # Handle QTD
    try:
      item_qtd = int(item_required("div", class_="quantity_small nowrap")[0].text)
    except Exception:
      item_qtd = 1

    if "item--" in item_required["data-id"]:
      item_id = int(item_required["data-id"].replace("item--", ""))
      item_requires[item_id] = item_qtd
      define = "item"

    elif "materialgroup--" in item_required["data-id"]:
      item_id = int(item_required["data-id"].replace("materialgroup--", ""))
      group_requires[item_id] = item_qtd
      define = "group"

    define_item(item_id, define)

  return item_requires, group_requires

# This function must return the item id and it's byproducts
def get_item_byproducts(row_tds):
  item_products = row_tds[7](item_id_find)
  byproducts = {}
  
  # first item is the item itself
  item_id = int(item_products[0]["data-id"].replace("item--", ""))
  define_item(item_id, "item")

  for item_product in item_products[1:]:
    item_aux_id = int(item_product["data-id"].replace("item--", ""))
    define_item(item_aux_id, "item")
    byproducts[item_aux_id] = DEFAULT_T1_T3_PROC

  return item_id, byproducts

# This functions allow to dump data to a JSON file
def save_definition(data, name):
  json_file_name = name + ".json"
  txt_file_name = name + ".txt"
  try:
    with open(json_file_name, encoding="utf8", mode="w") as f:
      json.dump(data, f, indent=4, ensure_ascii=False)
  except Exception as err:
    print("Failed to save " + name + " definiton due to" + str(err))
    with open(txt_file_name, encoding="utf8", mode="w") as f:
      f.write(data)

# This function will perform single event execution
def process_row(tds):
  recipe_dict = {}
  recipe_id = get_recipe_id(tds)

  recipe_dict["profission"] = get_item_profission(tds)

  # Select processing time
  processing_time = DEFAULT_PROCESSING_TIME
  if recipe_dict["profission"] == "Cooking":
    processing_time = DEFAULT_COOK_PROCESSING_TIME
  elif recipe_dict["profission"] == "Alchemy":
    processing_time = DEFAULT_ALCHEMY_PROCESSING_TIME

  recipe_dict["time_required"] = processing_time
  recipe_dict["item_requirements"], recipe_dict["group_requirements"] = get_item_requirements(tds)
  recipe_dict["generates"], recipe_dict["byproducts"] = get_item_byproducts(tds)
  recipe_dict["proc"] = DEFAULT_PROC_PER_PROCESS

  # Write to global var
  aux_recipes_cv.acquire()
  aux_recipes[recipe_id] = recipe_dict.copy()
  aux_recipes_cv.release()
  threadLimiter.release()

def generate_threads(file):

  aux_recipes_cv.acquire()
  aux_recipes = {}
  aux_recipes_cv.release()

  print ("Processing file " + file)
  with open(file, encoding="utf8") as fp:
    soup = BeautifulSoup(fp, features="html.parser")

  trs = soup.tbody("tr")
  bar = Bar('Loading', fill='@', suffix='%(percent).1f%% - %(eta)ds', max=len(trs))

  # Start threads
  thread_list = []
  for row in trs:
    bar.next()
    threadLimiter.acquire()
    t = threading.Thread(target=process_row, args=(row("td"),))
    thread_list.append(t)
    t.start()

  # Wait for threads to join
  for thread in thread_list: thread.join()

  bar.finish()

# Main function
def main():

  # Check if we have some itens ready
  load_item_definition()

  # Start processing stuff
  # generate_threads(PROCESSING_FILE)
  # save_definition(aux_recipes, "processing")
  generate_threads(CRAFTING_FILE)
  save_definition(aux_recipes, "crafting")

  # Save definitions
  save_definition(itens_definition, "itens_definition")
  save_definition(itens_group_definition, "itens_group_definition")

if __name__ == '__main__':
  main()