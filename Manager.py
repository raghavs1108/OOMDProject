from Database import Database
from QualityController import QualityController

class Manager:
	def __init__(self):
		self.db = Database()
		self.qc = QualityController()

	def checkAvailibility(self, item):
		itemInfo = self.db.getItemInfoFromInventory(item[0])
		if len(itemInfo) > 1:
			#item available
			if itemInfo[1] > item[1]:
				# sufficient quantity available
				return ["available", item[1]]
			else:
				# need to order more of that item
				return ["available", itemInfo[1]]
		else:
			#item not available
			return ["notAvailable"]

	def itemList(self):
		self.db.itemList()
		return

	def displayInventory(self):
		inventory = self.db.displayInventory()
		for i in inventory:
			print i

	def close(self):
		self.qc.close()
		self.db.close()

	def takeOrder(self, client_id):
		# print ("Since I'm just a computer program, make it simple. privide only the item ids to me..")
		# print ("Format: \nid1 count1 \nid2 count2 \nid3 count3 \nif you're done, press enter twice")
		print ("Client number:" + str(client_id))
		print ("tell me what you want:")
		self.items = []
		while True:
			ip = str(raw_input())
			if ip == "":
				break
			else :
				ip = (int(ip.split(" ")[0]),int(ip.split(" ")[1]))
				self.items.append(ip)
			print self.items

		print ("alright.. lets check their availability");
		self.notAvailable = []

		for item in self.items:
			availInfo = self.checkAvailibility(item)
			if availInfo[0] == "available":
				if availInfo[1] == item[1]:
					print "checking product quality...\n"
					quality = self.qc.checkQuality(item[0])
					if quality == "good":
						print "item ID "+str(item[0]) + " requested amount available"
					else :
						self.notAvailable.append(item)
						print "apologies.. the product available has expired.\n We will get back to you."
						self.qc.renewStock(item[0], item[1], client_id)
				else:
					# available, but not the requested quantity
					self.notAvailable.append(item)
					print "item ID "+str(item[0]) + " not available. Please wait. We will get back to you."
					self.qc.renewStock(item[0], item[1], client_id)
			else:
				# item isn't in the inventory
				self.notAvailable.append(item)
				print "item ID "+str(item[0]) + " not available. Please wait. We will get back to you."
				self.qc.renewStock(item[0], item[1], client_id)
				
		if len(self.notAvailable) == 0:
			# everything available
			return ["checkout", self.items]
		else:
			return ["don't checkout", self.notAvailable]