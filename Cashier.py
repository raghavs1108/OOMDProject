from Database import Database
class Cashier:
	def __init__(self):
		self.db = Database()
	def checkout(self, items):
		itemDetails = []
		for item in items:
			x = list(self.db.getItemDetails(item[0]))
			x.append(item[1])
			itemDetails.append(x)
		print itemDetails
		self.cost = []
		print "\n\n Summary: \n\n"
		for i in itemDetails:
			print "id = "+str(i[0])
			print "name = "+str(i[1])
			print "category = "+str(i[2])
			print "life time since date of manufacture(in days) = "+str(i[3])
			print "price = "+str(i[4])
			print "quantity = "+str(i[5])
			print "cost for that quantity = " + str(i[5] * i[4])
			self.cost.append(i[4]*i[5])
		print "net cost = " + str(sum(self.cost))

		answer = str(raw_input("proceed? yes/no"))
		if answer == "yes":
			print "purchase accepted."
			for item in items:
				self.db.updateInventory(item)
		else:
			print "no purchase"
		print "Thank you for visiting."
	def close(self):
		self.db.close()