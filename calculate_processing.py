import json

# Define percentage that you will loose due to market tax
MARKET_DEFAULT_TAX = (1-0.145)
DEFAULT_PROCESSING_PROC = 2.5

# Load definitions
PROCESSING_FILE = "data/processing.json"
ITENS_FILE = "data/itens.json"

try:
  with open(PROCESSING_FILE, "r") as read_file:
    processing_data = json.load(read_file)

  with open(ITENS_FILE, "r") as read_file:
    itens_data = json.load(read_file)

except Exception as err:
  print ("Could not load default JSON files. Aborting")
  print (err)
  exit(1)

# Define global vars
DEFAULT_WOOD_PROCESSING_TIME = processing_data["DEFAULT_WOOD_PROCESSING_TIME"]
DEFAULT_ORE_PROCESSING_TIME = processing_data["DEFAULT_ORE_PROCESSING_TIME"]
DEFAULT_T1_T3_ORE_PROC = processing_data["DEFAULT_T1_T3_ORE_PROC"]

# Generate profitability dict
profitable = {}
processing_data = processing_data["processing_itens"]

for item in processing_data:
  item_price = itens_data[item]
  requirements = processing_data[item]["requirements"]

  # Get price and value for each required item
  price_required = 0
  for required, qtd in requirements.items():
    price_required += itens_data[required]*qtd
  price_required *= MARKET_DEFAULT_TAX

  # price_required is the price you would get by selling stuff into market, e.g. without processing
  # Now let's calculate how much you get by processing.
  price_processing = item_price*DEFAULT_PROCESSING_PROC
  price_processing *= MARKET_DEFAULT_TAX
  profit = (price_processing-price_required)

  # Must set the profit you would do in an hour
  time_required = processing_data[item]["time_required"]
  if time_required == "DEFAULT_WOOD_PROCESSING_TIME":
    time_required = DEFAULT_WOOD_PROCESSING_TIME
  elif time_required == "DEFAULT_ORE_PROCESSING_TIME":
    time_required = DEFAULT_ORE_PROCESSING_TIME

  hour_to_seconds = 60*60 / time_required
  profitable[item] = int(profit*hour_to_seconds)

# Print itens
for item in sorted(profitable.items(), key=lambda x: x[1], reverse=True):
  print (item)