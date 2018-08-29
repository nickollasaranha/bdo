import json

# Define percentage that you will loose due to market tax
MARKET_DEFAULT_TAX = (1-0.145)
DEFAULT_PROC_PER_PROCESS = 2.5

# Load definitions
PROCESSING_DEFINITION_FILE = "data/processing_itens.json"
ITENS_DEFINITION_FILE = "data/itens_definition.json"
ITENS_GROUP_DEFINITION_FILE = "data/itens_group_definition.json"

DEFAULT_LANGUAGE = "pt"

try:
  with open(PROCESSING_DEFINITION_FILE, encoding="utf8", mode="r") as read_file:
    processing_data = json.load(read_file)

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
    return min(itens_price)

  return int(itens_data[item_id]["price"])

# This function returns the item profission
def get_item_profission(item_id):
  item_id = str(item_id)
  return processing_data[item_id]["profission"]

# This function returns the item name
def get_item_name(item_id):
	return itens_data[item_id]["name"][DEFAULT_LANGUAGE]

# This function will print the profitable things
def print_values(profitable):
	for item in sorted(profitable.items(), key=lambda k: k[1], reverse=True):
		print("Process type:", get_item_profission(item[0]), ">>", get_item_name(item[0]), ">>", item[1], "S/H")
  

# MAIN FUNC
def main():
  profitable = {}
  for item in processing_data:

    for item_aux in processing_data[item]:
      # Just to try
      if not (item == "4057"): continue
      print(item_aux)
      # We won't process things that has -1 as price (must set price)
      if get_item_price(item, "item") == -1: continue
      non_available_price_flag = False

      # Calculate required item price
      requirements_price = 0
      item_requirements = item_aux["item_requirements"]
      group_requirements = item_aux["group_requirements"]

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
      item_price = get_item_price(item, "item")*DEFAULT_PROC_PER_PROCESS
      item_price *= MARKET_DEFAULT_TAX

      # Calculate the profit by hour
      profit = (item_price-requirements_price)
      hour_to_seconds = 60*60 / item_aux["time_required"]
      profitable[item] = int(profit*hour_to_seconds)

  print_values(profitable)

if __name__ == '__main__':
  main()