from Manager import Manager
from Cashier import Cashier
import sys
import random

class Inventory:
	option = 0
	def selectOptions(self):
		print("press 1 to purchase:")
		print("press 2 to return:")
		print("press 3 to display Inventory:")
		return int(raw_input())

	def __init__(self):
		self.manager = Manager()
		self.cashier = Cashier()
		flag = True
		while flag:
			self.option = self.selectOptions()
			if self.option == 1:
				self.client_id = random.randint(1, 1000)
				self.manager.itemList()
				orderDetails = self.manager.takeOrder(self.client_id)
				if orderDetails[0] == "checkout":
					self.cashier.checkout(orderDetails[1])
					self.manager.displayInventory()
				elif orderDetails[0] == "don't checkout":
					print("we have ordered the requested items right away! please wait for us to get back to you.")
			elif self.option ==2:
				self.manager.close()
				self.cashier.close()
				flag = False
				sys.exit(0)
			elif self.option == 3:
				self.manager.displayInventory()

pharmacy = Inventory()