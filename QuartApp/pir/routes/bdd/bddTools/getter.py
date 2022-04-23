class Get():
	def __init__(self,bdd):
		self.cur = bdd.cur

	# Prendre juste Vues et Duree de chaque partie (ça sera averagé par date et scenario)
	# Faire un camembert

	# Même parti sur une chaine
	# Fais la moyenne des durées/vues sur toutes les dates
	def dateAverage(self):
		query = """SELECT parti, SUM(duree), CAST(SUM(vue) AS INT), COUNT(*)
				   FROM Video
				   GROUP BY parti"""
		self.cur.execute(query)
		return self.cur.fetchall()

	# Expo d'un parti entier en fonction de l'avancement dans le temps
	def candidatExpoEvol(self,parti):
		query = """SELECT (SUM(duree)*SUM(vue))/1000000000 AS expo, date
	 			   FROM Video
				   WHERE parti = %s
				   GROUP BY parti, date
	 			   ORDER BY date"""
		self.cur.execute(query,(parti,))
		return self.cur.fetchall()

	# Expo d'un parti par ses soutien en fonction de l'avancement dans le temps
	def soutienExpoEvol(self,parti,soutien):
		query = """SELECT (SUM(duree)*SUM(vue))/1000000000 AS expo, date
	 			   FROM Video
				   WHERE parti = %s and soutien = %s
				   GROUP BY parti, date
	 			   ORDER BY date"""
		self.cur.execute(query,(parti,soutien))
		return self.cur.fetchall()

	# Exposition des candidats par prof
	def candidatDepthEvol(self,parti,prof):
		query = """SELECT date,SUM(duree),CAST(SUM(vue) AS INT)
				   FROM Video
				   WHERE 
				   		parti = %s AND
				   		profondeur = %s 
				   GROUP BY parti,date,profondeur
				   ORDER BY date"""
		self.cur.execute(query,(parti,prof))
		return self.cur.fetchall()

	# Exposition des candidats par prof
	def candidatDepth(self,parti):
		query = """SELECT SUM(duree)*CAST(SUM(vue) AS INT), profondeur
				   FROM Video
				   WHERE 
				   		parti = %s 
				   GROUP BY parti,profondeur"""
		self.cur.execute(query,(parti,))
		return self.cur.fetchall()
		
	# D'où vient l'exposition de chaque candidat
	def scenarioParti(self,parti):
		query = """SELECT scenario, SUM(duree), CAST(SUM(vue) AS INT)
					FROM Video 
					WHERE parti = %s
					GROUP BY scenario,parti"""
		self.cur.execute(query,(parti,))
		return self.cur.fetchall()

	def allPartis(self):
		self.cur.execute("""SELECT DISTINCT parti
				            FROM Video""")
		partis = self.cur.fetchall()
		return [x[0] for x in partis]

	def allSoutiens(self,parti):
		query = """SELECT DISTINCT soutien
				    FROM Video
					WHERE parti = %s"""
		self.cur.execute(query,(parti,))
		soutiens = self.cur.fetchall()
		return [x[0] for x in soutiens]

