import "item.py"

PROCESSING_NAME = "PROCESSAMENTO"
PROCESSING_REQUIRED_ITEM = 10
PROCESSING_PROC = 2.5 # each 10 itens generates 2,5 itens
DEFAULT_TAX_MARKET = (1 - 0.155) # 15.5% tax
DEFAULT_WOOD_PROCESSING_TIME = 4
DEFAULT_ORE_PROCESSING_TIME = 13

ITENS = []

# Aux Functions
def get_upgraded_item(item):
	return [aux_item["upgrades_to"] for aux_item in ITENS if aux_item["name"] == item][0]

def get_item_cost(item):
	return [aux_item["price"] for aux_item in ITENS if aux_item["name"] == item][0]

def get_item_required_time(item):
	return [aux_item["required_time"] for aux_item in ITENS if aux_item["name"] == item][0]

def create_item(name, profission, required_time, upgrades_to):
	return {"name": name, "profission": profission, "required_time": required_time, "upgrades_to": upgrades_to}

# ITEM VARS
# Woods
freixo_t1 = create_item("freixo_t1", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "freixo_t2")
freixo_t2 = create_item("freixo_t2", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "freixo_t3")
freixo_t3 = create_item("freixo_t3", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, None)
bordo_t1 = create_item("bordo_t1", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "bordo_t2")
bordo_t2 = create_item("bordo_t2", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "bordo_t3")
bordo_t3 = create_item("bordo_t3", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, None)
betula_t1 = create_item("betula_t1", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "betula_t2")
betula_t2 = create_item("betula_t2", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "betula_t3")
betula_t3 = create_item("betula_t3", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, None)
pinheiro_t1 = create_item("pinheiro_t1", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "pinheiro_t2")
pinheiro_t2 = create_item("pinheiro_t2", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, "pinheiro_t3")
pinheiro_t3 = create_item("pinheiro_t3", PROCESSING_NAME, DEFAULT_WOOD_PROCESSING_TIME, None)
ITENS.append(freixo_t1)
ITENS.append(freixo_t2)
ITENS.append(freixo_t3)
ITENS.append(bordo_t1)
ITENS.append(bordo_t2)
ITENS.append(bordo_t3)
ITENS.append(betula_t1)
ITENS.append(betula_t2)
ITENS.append(betula_t3)
ITENS.append(pinheiro_t1)
ITENS.append(pinheiro_t2)
ITENS.append(pinheiro_t3)

# Ores
iron_t1 = create_item("iron_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "iron_t2")
iron_t2 = create_item("iron_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "iron_t3")
iron_t3 = create_item("iron_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
copper_t1 = create_item("copper_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "copper_t2")
copper_t2 = create_item("copper_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "copper_t3")
copper_t3 = create_item("copper_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
estanho_t1 = create_item("estanho_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "estanho_t2")
estanho_t2 = create_item("estanho_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "estanho_t3")
estanho_t3 = create_item("estanho_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
zinco_t1 = create_item("zinco_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "zinco_t2")
zinco_t2 = create_item("zinco_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "zinco_t3")
zinco_t3 = create_item("zinco_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
ITENS.append(iron_t1)
ITENS.append(iron_t2)
ITENS.append(iron_t3)
ITENS.append(copper_t1)
ITENS.append(copper_t2)
ITENS.append(copper_t3)
ITENS.append(estanho_t1)
ITENS.append(estanho_t2)
ITENS.append(estanho_t3)
ITENS.append(zinco_t1)
ITENS.append(zinco_t2)
ITENS.append(zinco_t3)

# PRICE ITEM
freixo_t1["price"] = 605
freixo_t2["price"] = 2093
freixo_t3["price"] = 9848

bordo_t1["price"] = 649
bordo_t2["price"] = 2341
bordo_t3["price"] = 11549

betula_t1["price"] = 693
betula_t2["price"] = 2772
betula_t3["price"] = 10080

pinheiro_t1["price"] = 777
pinheiro_t2["price"] = 3117
pinheiro_t3["price"] = 24948

iron_t1["price"] = 539
iron_t2["price"] = 2500
iron_t3["price"] = 13389

copper_t1["price"] = 471
copper_t2["price"] = 1288
copper_t3["price"] = 12995

estanho_t1["price"] = 539
estanho_t2["price"] = 2636
estanho_t3["price"] = 12091

zinco_t1["price"] = 1058
zinco_t2["price"] = 3469
zinco_t3["price"] = 15422

def process_silver(item):

	upgraded_item = get_upgraded_item(item)
	if upgraded_item is None: return [item, 0]

	item_price = get_item_cost(item)

	# Default price if you sell to market
	market_price_per_pack = (item_price*10)*DEFAULT_TAX_MARKET

	# This is the default price of processing item.
	process_price = get_item_cost(upgraded_item)*PROCESSING_PROC

	# Added t3 proc if it's a T1
	if "t1" in item:
		t3_item_cost = get_item_cost(get_upgraded_item(upgraded_item))
		process_price += t3_item_cost*0.03*PROCESSING_PROC

	# Add DEFAULT_TAX_MARKET
	process_price *= DEFAULT_TAX_MARKET
	profit_processing = (process_price-market_price_per_pack)

	# Calculate profit_per_hour
	hour_to_seconds = 60*60 / get_item_required_time(item)

	# Return item name, profit per hour
	return [item, profit_processing*hour_to_seconds]

# MAIN
full_list = [process_silver(item_aux["name"]) for item_aux in ITENS]
print(sorted(full_list, key=lambda v: v[1], reverse=True))