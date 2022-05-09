from dotenv import load_dotenv
import os 

import mariadb
import threading
import time

class BDD():

	def __init__(self):
		self.conn = None
		self.timer = 0
		self.timerMax = 600

	def connect(self):

		try:
			self.conn = mariadb.connect(
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

	def disconnect(self):
		self.conn.close()

# ---- Dotenv

load_dotenv()
user = os.getenv('DB_User_Pir')
password = os.getenv('DB_Password_Pir')
host = os.getenv('DB_Host_Pir')
port = int(os.getenv('DB_Port_Pir'))
db = os.getenv('DB_db_Pir')

bdd = BDD()

def timer():
	while(True):
		time.sleep(1)
		if bdd.timer > 0 :
			bdd.timer -= 1

t1 = threading.Thread(target=timer, args=[])
t1.start()

# ---- Connect

def bddConnect(function):

	def wrapper(*args, **kwargs):

		if bdd.timer < 1 : 
			bdd.connect()

		# Fonction
		res = function(bdd.conn.cursor(), *args, **kwargs)
		bdd.timer = bdd.timerMax
		return res

	return wrapper

# ------------ GET Functions

# Même parti sur une chaine
# Fais la moyenne des durées/vues sur toutes les dates
@bddConnect
def dateAverage(cur):
	query = """SELECT parti, SUM(duree), CAST(SUM(vue) AS INT), COUNT(*)
				FROM Video
				GROUP BY parti"""
	cur.execute(query)
	return cur.fetchall()

# Expo d'un parti entier en fonction de l'avancement dans le temps
@bddConnect
def candidatExpoEvol(cur,parti):
	query = """SELECT (SUM(duree)*SUM(vue))/1000000000 AS expo, date
				FROM Video
				WHERE parti = %s
				GROUP BY parti, date
				ORDER BY date"""
	cur.execute(query,(parti,))
	return cur.fetchall()

# Expo d'un parti par ses soutien en fonction de l'avancement dans le temps
@bddConnect
def soutienExpoEvol(cur,parti,soutien):
	query = """SELECT (SUM(duree)*SUM(vue))/1000000000 AS expo, date
				FROM Video
				WHERE parti = %s and soutien = %s
				GROUP BY parti, date
				ORDER BY date"""
	cur.execute(query,(parti,soutien))
	return cur.fetchall()

# Exposition des candidats par prof
@bddConnect
def bddCandidatDepthEvol(cur,parti,prof):
	query = """SELECT date,SUM(duree),CAST(SUM(vue) AS INT)
				FROM Video
				WHERE 
					parti = %s AND
					profondeur = %s 
				GROUP BY parti,date,profondeur
				ORDER BY date"""
	cur.execute(query,(parti,prof))
	return cur.fetchall()

# Exposition des candidats par prof
@bddConnect
def candidatDepth(cur,parti):
	query = """SELECT SUM(duree)*CAST(SUM(vue) AS INT), profondeur
				FROM Video
				WHERE 
					parti = %s 
				GROUP BY parti,profondeur"""
	cur.execute(query,(parti,))
	return cur.fetchall()
	
# D'où vient l'exposition de chaque candidat
@bddConnect
def scenarioParti(cur,parti):
	query = """SELECT scenario, SUM(duree), CAST(SUM(vue) AS INT)
				FROM Video 
				WHERE parti = %s
				GROUP BY scenario,parti"""
	cur.execute(query,(parti,))
	return cur.fetchall()

# ------------ GET Infos

@bddConnect
def allPartis(cur):
	cur.execute("""SELECT DISTINCT parti
						FROM Video""")
	partis = cur.fetchall()
	return [x[0] for x in partis]

@bddConnect
def allSoutiens(cur,parti):
	query = """SELECT DISTINCT soutien
				FROM Video
				WHERE parti = %s"""
	cur.execute(query,(parti,))
	soutiens = cur.fetchall()
	return [x[0] for x in soutiens]







if __name__ == "__main__" :

	print(allPartis())
	
	
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

	# query = """SELECT SUM(duree)*CAST(SUM(vue) AS INT)
	# 			   FROM Video
	# 			   WHERE 
	# 			   		parti = %s AND
	# 			   		profondeur in (1,2,5)
	# 			   GROUP BY parti,profondeur"""
	# bdd.cur.execute(query,("MELENCHON",))
	# x = bdd.cur.fetchall()
	# x = [y[0] for y in x]
	# print(x)