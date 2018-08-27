class Item:
	def __init__(self, name, profession, time_required, requirements):
		self.name = name
		self.profession = None
		self.time_required = 0
		self.requirements = {}

  def set_price(self, price):
		self.price = price