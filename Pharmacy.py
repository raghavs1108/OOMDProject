from Manager import Manager
from Cashier import Cashier
import sys

class Inventory:
	option = 0
	def selectOptions(self):
		print("press 1 to purchase:")
		print("press 2 to return:")
		return int(raw_input())

	def __init__(self):
		self.manager = Manager()
		self.cashier = Cashier()
		flag = True
		while flag:
			self.option = self.selectOptions()
			if self.option == 1:
				self.manager.itemList()
				orderDetails = self.manager.takeOrder()
				if orderDetails[0] == "checkout":
					self.cashier.checkout(orderDetails[1])
					self.manager.displayInventory()
				elif orderDetails[0] == "don't checkout":
					print("we'll order the requested items right away! please wait for us to get back to you.")
			else:
				self.manager.close()
				self.cashier.close()
				flag = False
				sys.exit(0)

pharmacy = Inventory()