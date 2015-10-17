from Database import Database
from Supplier import Supplier
import datetime
import threading
import time

class QualityController:
	def deleteItemFromInventory(self, i):
		self.db.deleteItemFromInventory(i)

	def addItemToInventory(self, item_id, quantity):
		now  = time.strftime("%Y-%m-%d")
		self.db.addItemToInventory(item_id, quantity, now)

	def checkExpiry(self):
		while True:
			time.sleep(60)
			for i in self.db.displayInventory():
				quality = self.checkQuality(i[0])
				if quality == "good":
					pass
				else:
					print "expiry found. Item removed from inventory."

	def renewStock(self, item_id, quantity):
		itemDetails = self.db.getItemDetails(item_id)
		self.supplier.request((itemDetails[0], itemDetails[1]), quantity)
		# assume that the request is fulfilled..
		self.addItemToInventory(item_id, quantity)

	def close(self):
		self.db.close()

	def __init__(self):
		self.renewQuantity = 10
		self.db = Database()
		self.supplier = Supplier()
		t = threading.Thread(target=self.checkExpiry, args="")
		t.start()

	def checkQuality(self, item_id):
		ttl = self.db.getItemDetails(item_id)[3]
		date_of_purchase = str(self.db.getItemInfoFromInventory(item_id)[2])
		y = date_of_purchase.split("-")[0]
		m = date_of_purchase.split("-")[1]
		d = date_of_purchase.split("-")[2]
		date_of_purchase = "/".join([m,d,y])
		date_of_purchase = datetime.datetime.strptime(date_of_purchase, "%m/%d/%Y")
		end_date = date_of_purchase + datetime.timedelta(days=ttl)
		now = datetime.datetime.now()

		if now < end_date:
			print "end_date not reached."
			print "good quality."
			return "good"
		else:
			print "end date reached."
			print "bad quality."
			self.deleteItemFromInventory(item_id)
			t = threading.Thread(target=self.renewStock, args=(item_id, self.renewQuantity))
			t.start()
		return "not good"