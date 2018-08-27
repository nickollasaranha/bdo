import "item.py"

ITENS = []

# Aux Functions
def get_upgraded_item(item):
	return [aux_item["upgrades_to"] for aux_item in ITENS if aux_item["name"] == item][0]

def get_item_cost(item):
	return [aux_item["price"] for aux_item in ITENS if aux_item["name"] == item][0]

def get_item_required_time(item):
	return [aux_item["required_time"] for aux_item in ITENS if aux_item["name"] == item][0]

# ITEM VARS
# Woods

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
iron_t1 = Item("iron_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "iron_t2")
iron_t2 = Item("iron_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "iron_t3")
iron_t3 = Item("iron_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
copper_t1 = Item("copper_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "copper_t2")
copper_t2 = Item("copper_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "copper_t3")
copper_t3 = Item("copper_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
estanho_t1 = Item("estanho_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "estanho_t2")
estanho_t2 = Item("estanho_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "estanho_t3")
estanho_t3 = Item("estanho_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
zinco_t1 = Item("zinco_t1", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "zinco_t2")
zinco_t2 = Item("zinco_t2", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, "zinco_t3")
zinco_t3 = Item("zinco_t3", PROCESSING_NAME, DEFAULT_ORE_PROCESSING_TIME, None)
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
freixo_t1.set_price(605)
freixo_t2.set_price(2093)
freixo_t3.set_price(9848)

bordo_t1.set_price(649)
bordo_t2.set_price(2341)
bordo_t3.set_price(11549)

betula_t1.set_price(693)
betula_t2.set_price(2772)
betula_t3.set_price(10080)

pinheiro_t1.set_price(777)
pinheiro_t2.set_price(3117)
pinheiro_t3.set_price(24948)

iron_t1.set_price(539)
iron_t2.set_price(2500)
iron_t3.set_price(13389)

copper_t1.set_price(471)
copper_t2.set_price(1288)
copper_t3.set_price(12995)

estanho_t1.set_price(539)
estanho_t2.set_price(2636)
estanho_t3.set_price(12091)

zinco_t1.set_price(1058)
zinco_t2.set_price(3469)
zinco_t3.set_price(15422)

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