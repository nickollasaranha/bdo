import json

# Define percentage that you will loose due to market tax
MARKET_DEFAULT_TAX = (1-0.145)
DEFAULT_PROC_PER_PROCESS = 2.5

# Load definitions
PROCESSING_DEFINITION_FILE = "data/processing.json"
CRAFTING_DEFINITION_FILE = "data/crafting.json"
ITENS_DEFINITION_FILE = "data/itens_definition.json"
ITENS_GROUP_DEFINITION_FILE = "data/itens_group_definition.json"

DEFAULT_LANGUAGE = "pt"

try:
  with open(PROCESSING_DEFINITION_FILE, encoding="utf8", mode="r") as read_file:
    processing_data = json.load(read_file)

  with open(CRAFTING_DEFINITION_FILE, encoding="utf8", mode="r") as read_file:
    crafting_data = json.load(read_file)

  with open(ITENS_DEFINITION_FILE, encoding="utf8", mode="r") as read_file:
    itens_data = json.load(read_file)

  with open(ITENS_GROUP_DEFINITION_FILE, encoding="utf8", mode="r") as read_file:
    group_data = json.load(read_file)
except Exception as err:
  print ("Could not load default JSON files. Aborting")
  print (err)
  exit(1)

# This function returns the item or group price
def get_item_price(item_id, tipo):
  # ID must be a string
  item_id = str(item_id)
  # Must check if it's an item or group.
  if tipo=="group":
    # We will get the min value of the group
    itens_price = []
    itens = group_data[item_id]["itens"]
    for aux_item_id in itens: itens_price.append(get_item_price(aux_item_id, "item"))
    return min([price for price in itens_price if price!=-1])
  return int(itens_data[item_id]["price"])

# This function returns the recipe profission
def get_recipe_profission(recipe_id, tipo):
  if tipo == "crafting":
    return crafting_data[recipe_id]["profission"]
  elif tipo == "processing":
    return processing_data[recipe_id]["profission"]

# This function returns the item name
def get_item_name(item_id):
  return itens_data[str(item_id)]["name"][DEFAULT_LANGUAGE]

# This function returns recipe generating item
def get_recipe_generate_item(recipe_id, tipo):
  if tipo == "crafting":
    return get_item_name(crafting_data[recipe_id]["generates"])
  elif tipo == "processing":
    return get_item_name(processing_data[recipe_id]["generates"])

# This function will print the profitable things
def print_values(profitability_list):

  for item in sorted(profitability_list, key=lambda k:list(k.values())[0][1], reverse=True):
    tipo = list(item.keys())[0]
    recipe_id = list(item.values())[0][0]
    item_generating = get_recipe_generate_item(recipe_id, tipo)
    profission = get_recipe_profission(recipe_id, tipo)
    profitability = list(item.values())[0][1]
    print("Process type:", profission, ">>", item_generating, ">>", "{:,}".format(profitability), "S/H")

def calcProfitability(data, name):
  profitability_list = []
# Process itens
  for recipe_id in data:
    recipe_id = str(recipe_id)
    generating_item = data[recipe_id]["generates"]

    # We won't process things that has -1 as price (must set price)
    if get_item_price(generating_item, "item") == -1: continue
    non_available_price_flag = False

    # Calculate required item price
    requirements_price = 0
    item_requirements = data[recipe_id]["item_requirements"]
    group_requirements = data[recipe_id]["group_requirements"]

    for aux_item_id, qtd in item_requirements.items():
      aux_item_price = get_item_price(aux_item_id, "item")
      if aux_item_price == -1: non_available_price_flag = True
      requirements_price+=(aux_item_price*qtd)
    for aux_group_id, qtd in group_requirements.items(): 
      aux_group_price = get_item_price(aux_group_id, "group")
      if aux_item_price == -1: non_available_price_flag = True
      requirements_price+=(aux_group_price*qtd)

    # Won't calculate unavailable requirements
    if non_available_price_flag: continue

    # This is the price of selling the material to the market
    requirements_price *= MARKET_DEFAULT_TAX

    # Calculate the item price now.
    item_price = get_item_price(generating_item, "item")*DEFAULT_PROC_PER_PROCESS
    item_price *= MARKET_DEFAULT_TAX

    # Calculate the profit by hour
    profit = (item_price-requirements_price)
    hour_to_seconds = 60*60 / data[recipe_id]["time_required"]
    profitability_list.append({name: [recipe_id, int(profit*hour_to_seconds)]})

  return profitability_list

# MAIN FUNC
def main():

  # Calc processing and crafting
  processing_profitability = calcProfitability(processing_data, "processing")
  crafting_profitability = calcProfitability(crafting_data, "crafting")
  profitability_list = processing_profitability+crafting_profitability
  print_values(profitability_list)

if __name__ == '__main__':
  main()