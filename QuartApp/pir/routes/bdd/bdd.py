if __name__ == '__main__' :
	from bddTools import *
else :
	from .bddTools import *

from dotenv import load_dotenv
import os 

import mariadb

class BDD():

	def __init__(self):

		load_dotenv()
		user = os.getenv('DB_User_Pir')
		password = os.getenv('DB_Password_Pir')
		host = os.getenv('DB_Host_Pir')
		port = int(os.getenv('DB_Port_Pir'))
		db = os.getenv('DB_db_Pir')

		try:
			conn = mariadb.connect(
				user=user,
				password=password,
				host=host,
		  		port=port,
		  		database=db
			)
			print("Connecté à la BDD de {} sur le port {}".format(host,port))

		except mariadb.Error as e:
			print(f"Error connecting to MariaDB Platform: {e}")
			exit()

		self.conn = conn
		self.cur = conn.cursor()
		self.get = Get(self)

	def request(self,req,args):
		return self.cur.execute(req,args)

	def commit(self):
		self.conn.commit()

if __name__ == "__main__" :
	
	bdd = BDD()
	
	# bdd.manage.renewTables()
	# bdd.manage.createTables()

	# bdd.cur.execute("""SELECT parti,date,profondeur, COUNT(*)
	# 			   FROM Video
	# 			   WHERE 
	# 			   		parti = "LASSALLE" AND
	# 			   		profondeur IN (1,2,5)  
	# 			   GROUP BY parti,date,profondeur
	# 			   ORDER BY date""")

	# bdd.cur.execute("SELECT DISTINCT scenario FROM Video")
	# bdd.cur.execute("DESCRIBE Video")

	# bdd.cur.execute("""SELECT soutien, (SUM(duree)*SUM(vue))/1000000000 AS expo, date, COUNT(*)
	#  			   FROM Video
	# 			   WHERE parti = 'MELENCHON'
	# 			   GROUP BY parti, date, soutien
	#  			   ORDER BY date""")

	# for x in bdd.cur :
	# 	print(x)


	# print( bdd.get.scenarioParti("HIDALGO"))
	# a,x,y = bdd.get.scenarioParti("HIDALGO")
	# print(sum(x)*sum(y))


	# print(bdd.get.allSoutiens("MELENCHON"))

	query = """SELECT SUM(duree)*CAST(SUM(vue) AS INT)
				   FROM Video
				   WHERE 
				   		parti = %s AND
				   		profondeur in (1,2,5)
				   GROUP BY parti,profondeur"""
	bdd.cur.execute(query,("MELENCHON",))
	x = bdd.cur.fetchall()
	x = [y[0] for y in x]
	print(x)