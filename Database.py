import MySQLdb

conn = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="password", # your password
                      db="pharmacy") # name of the data base
cur = conn.cursor()

class Database :
	def createAllTables(self):
		query = "CREATE TABLE IF NOT EXISTS category(category_id int primary key, category_name text);"
		cur.execute(query)
		query = "CREATE TABLE IF NOT EXISTS item(item_id int  primary key, item_name text, category_id int, ttl int, price int, CONSTRAINT FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE);"
		cur.execute(query)
		query = "CREATE TABLE IF NOT EXISTS inventory(item_id int, item_count int, date_of_purchase DATE, CONSTRAINT PRIMARY KEY(item_id, date_of_purchase));"
		cur.execute(query)
		query = "CREATE TABLE IF NOT EXISTS pending_orders(client_id int,item_id int, item_count int);"
		cur.execute(query)
		return 

	def dropAllTables(self):
		query = "DROP TABLE inventory;"
		cur.execute(query)
		query = "DROP TABLE pending_orders;"
		cur.execute(query)
		query = "DROP TABLE item;"
		cur.execute(query)
		query = "DROP TABLE category;"
		cur.execute(query)
		return

	def deleteAllData(self):
		query = "DELETE FROM category;"
		cur.execute(query)
		query = "DELETE FROM item;"
		cur.execute(query)
		query = "DELETE FROM inventory;"
		cur.execute(query)
		query = "DELETE FROM pending_orders;"
		cur.execute(query)
		conn.commit()
		return 

	def insertAllData(self):
		values = [
  			(1, "allergenics"),
  			(2, "anorexiants"),
  			(3, "antacids")
		]
		cur.executemany("""
        	insert into category (category_id, category_name) values (%s, %s);""", values)
		conn.commit()
		

		values = [
			(1, "grastek", 1, 90, 50),
			(2, "oralair", 1, 100, 20),
			(3, "prelu-2", 2, 150, 10),
			(4, "Suprenza", 2, 100, 25),
			(5, "DiGel", 3, 100, 5)
		]
		cur.executemany("""
        	insert into item (item_id, item_name, category_id, ttl, price) values (%s, %s, %s, %s, %s);""", values)

		conn.commit()

		values = [
			(1, 10, '2015-12-15'),
			(2, 10, '2015-12-15'),
			(3, 10, '2015-12-15'),
			(4, 10, '2015-12-15'),
			(5, 10, '2015-12-15')
		]
		cur.executemany("""
        	insert into inventory (item_id, item_count, date_of_purchase) values (%s, %s, %s);""", values)
		conn.commit()
		return

	def itemList(self):
		query = "SELECT * FROM item;"
		cur.execute(query)
		for x in cur.fetchall():
			print x
	def updateInventory(self, item):
		query = "SELECT item_count FROM inventory WHERE item_id="+str(item[0])
		cur.execute(query)
		prev_val = int(cur.fetchone()[0])
		query = "UPDATE inventory SET item_count="+str(prev_val - item[1])+" where item_id="+str(item[0])
		cur.execute(query)

	def getItemInfoFromInventory(self, item_id):
		query = "SELECT * FROM inventory where item_id="+str(item_id)
		cur.execute(query)
		res = cur.fetchone()
		return res 

	def getItemDetails(self, item_id):
		query = "SELECT * FROM item where item_id="+str(item_id)
		cur.execute(query)
		return cur.fetchone()

	def __init__(self):
		self.dropAllTables()
		self.createAllTables()
		self.deleteAllData()
		self.insertAllData()
		return
	def displayInventory(self):
		query = "SELECT * from inventory"
		cur.execute(query)
		return cur.fetchall()
	def deleteItemFromInventory(self, item_id):
		query = "SELECT * from inventory where item_id="+item_id
		cur.execute(query)
		conn.commit()

	def addItemToInventory(self, item_id, quantity, date):
		cur.execute("""
        	insert into inventory (item_id, item_count, date_of_purchase) values (%s, %s, %s);""", (item_id, quantity, date))
		conn.commit()
	def close(self):
		try:
			cur.close()
			conn.close()
		except Exception as e:
			pass