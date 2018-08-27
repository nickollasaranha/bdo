class Item:
	def __init__(self, name, profession, time_required, requirements):
		self.name = name
		self.profession = None
		self.time_required = 0
		self.requirements = {}

		self.price = 0

a = Item("Freixo")
a.price = 200

print(a.price)