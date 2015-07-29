from django.conf import settings
from ssme_activities.models import CentreDeSante, CentreDeDistribution, PhoneNumber, Reporter, CentreDeDistributionReporters, StockDebutJournee, Report, StockRecuLeMatin, StockFinal, Beneficiaires, Medicament, RapportRupture, NiveauAvancement
import re
from datetime import datetime


class StockDebutJourneeControler():
	'''This class control a message for a pregnancy confirmation report'''
	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."
	
	def check_cds(self, data):
		''' This function checks if the CDS code exists in the system '''
		sent_cds_code = data['text'].split('+')[1]
		the_concerned_cds = CentreDeSante.objects.filter(code = sent_cds_code)
		if len(the_concerned_cds) < 1:
			data['valide'] = False
			data['response'] = "Le code du CDS envoye ("+sent_cds_code+") n est pas valide.  Veuillez reenvoyer votre message. Merci."
		else:
			data['cds'] = the_concerned_cds[0]
			data['cds_code'] = data['text'].split('+')[1]
	
	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[2]
		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recoding the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[2]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return

	def check_concerned_date(self, data):
		'''This function checks if the report date is a valid date''' 
		expression = r'^((0[1-9])|([1-2][0-9])|(3[01])).((0[1-9])|(1[0-2])).[0-9]{4}$'
		if re.search(expression, data['text'].split('+')[3]) is None:
			data['valide'] = False
			data['response'] = "Vous avez envoye une date non valide. Veuillez reenvoyer le message avec une date bien ecrite. ex: 30.02.2011"
		else:
			the_year = data['text'].split('+')[3].split('.')[2]
			the_month = data['text'].split('+')[3].split('.')[1]
			the_day = data['text'].split('+')[3].split('.')[0]
			data['the_date'] = the_year+"-"+the_month+"-"+the_day
			#data['the_date'] = data['text'].split('+')[3]

	def check_vitA_100000ui(self, data):
		''' This function checks if a quantity sent for vit A 100 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[4]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 100 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA100000UI'] = data['text'].split('+')[4]

	def check_vitA_200000ui(self, data):
		''' This function checks if a quantity sent for vit A 200 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[5]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 200 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA200000UI'] = data['text'].split('+')[5]

	def check_albendazole_400_mg(self, data):
		''' This function checks if a quantity sent for Albendazole is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[6]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour Albendazole n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Alb'] = data['text'].split('+')[6]

	def check_var2(self, data):
		'''This function checks if a quantity sent for VAR2 is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[7]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour VAR2 n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Var2'] = data['text'].split('+')[7]

	def check_mnp(self, data):
		'''This function checks if a quantity sent for MNP is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[8]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour MNP n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['mnp'] = data['text'].split('+')[8]

	def save_report(self, data):
		''' This function is used to save a well written report '''
		
		the_saved_report = Report.objects.create(reporter = data['reporter'],cdd = data['CDD'],text = data['text'],date = datetime.now(), the_concerned_date = data['the_date'], report_type ='SDJ' )
		
		the_specific_part_of_sms = StockDebutJournee.objects.create(code_cds = data['cds_code'],nom_site = data['CDD_name'],date = data['the_date'],vitA_100000ui = data['VitA100000UI'],vitB_200000ui = data['VitA200000UI'],albendazole = data['Alb'],var2 = data['Var2'],mnp = data['mnp'],report = the_saved_report)

		#Let's create a session
		the_session = NiveauAvancement.objects.create(reporter = data['reporter'], niveau = 1, the_concerned_date = the_saved_report.the_concerned_date, cdd_name = data['CDD'].name)
	

	
	def check_report(self, data):
		'''This method is the main checker'''
		print(".............................................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True



		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		#Let's check if the CDS (Centre de sante) sent is known in the system.
		self.check_cds(data)
		if not data['valide']:
			return

		#Let's check if the CDD (Centre de distribution) sent is known in the system
		#and that reporter is registered to report for that CDD
		self.check_site_name(data)
		if not data['valide']:
			return

		#Let's check if the date sent by the reporter is valid
		self.check_concerned_date(data)
		if not data['valide']:
			return

		#Let's check if the quantity (in the morning) of Vit A 100 000 UI sent by the reporter is valid
		self.check_vitA_100000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity (in the morning) of Vit A 200 000 UI sent by the reporter is valid
		self.check_vitA_200000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity (in the morning) of Albendazole sent by the reporter is valid
		self.check_albendazole_400_mg(data)
		if not data['valide']:
			return

		#Let's check if the quantity (in the morning) of VAR2 sent by the reporter is valid
		self.check_var2(data)
		if not data['valide']:
			return

		#Let's check if the quantity (in the morning) of MNP sent by the reporter is valid
		self.check_mnp(data)
		if not data['valide']:
			return

		#Let's save the report
		self.save_report(data)
		if not data['valide']:
			return




#-----------------------------------------------------------------------------------------------------------------------------------------




class StockRecuLeMatinControler():

	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."

	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[1]

		if data['session'].cdd_name != sent_cdd_name:
			data['valide'] = False
			data['response'] = "Message non enregistre. Vous n avez pas encore termine avec "+data['session'].cdd_name+"."
			return		

		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recoding the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[1]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return


	def check_vitA_100000ui(self, data):
		''' This function checks if a quantity sent for vit A 100 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[2]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 100 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA100000UI'] = data['text'].split('+')[2]

	def check_vitA_200000ui(self, data):
		''' This function checks if a quantity sent for vit A 200 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[3]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 200 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA200000UI'] = data['text'].split('+')[3]

	def check_albendazole_400_mg(self, data):
		''' This function checks if a quantity sent for Albendazole is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[4]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour Albendazole n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Alb'] = data['text'].split('+')[4]

	def check_var2(self, data):
		'''This function checks if a quantity sent for VAR2 is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[5]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour VAR2 n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Var2'] = data['text'].split('+')[5]

	def check_mnp(self, data):
		'''This function checks if a quantity sent for MNP is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[6]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour MNP n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['mnp'] = data['text'].split('+')[6]

	def save_report(self, data):
		''' This function is used to save a well written report '''
		the_saved_report = Report.objects.create(reporter = data['reporter'],cdd = data['CDD'],text = data['text'],date = datetime.now(),the_concerned_date = data['session'].the_concerned_date ,report_type ='SR' )
		
		the_specific_part_of_sms = StockRecuLeMatin.objects.create(vitA_100000ui = data['VitA100000UI'],vitB_200000ui = data['VitA200000UI'],albendazole = data['Alb'],var2 = data['Var2'],mnp = data['mnp'],report = the_saved_report)

		#Let's update a session
		data['session'].niveau = 2
		data['session'].save()



	def check_report(self, data):
		'''This method is the main checker'''
		print("..........................check_report debut...................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True


		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		#Let's check if the CDD (Centre de distribution) sent is known in the system
		#and that reporter is registered to report for that CDD
		self.check_site_name(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Vit A 100 000 UI sent by the reporter is valid
		self.check_vitA_100000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Vit A 200 000 UI sent by the reporter is valid
		self.check_vitA_200000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Albendazole sent by the reporter is valid
		self.check_albendazole_400_mg(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of VAR2 sent by the reporter is valid
		self.check_var2(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of MNP sent by the reporter is valid
		self.check_mnp(data)
		if not data['valide']:
			return

		#Let's save the report
		self.save_report(data)
		if not data['valide']:
			return





#-----------------------------------------------------------------------------------------------------------------------------------------





class StockFinalControler():

	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."

	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[1]

		if data['session'].cdd_name != sent_cdd_name:
			data['valide'] = False
			data['response'] = "Message non enregistre. Vous n avez pas encore termine avec "+data['session'].cdd_name+"."
			return

		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recoding the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[1]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return


	def check_vitA_100000ui(self, data):
		''' This function checks if a quantity sent for vit A 100 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[2]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 100 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA100000UI'] = data['text'].split('+')[2]

	def check_vitA_200000ui(self, data):
		''' This function checks if a quantity sent for vit A 200 000 UI is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[3]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour le Vit A 200 000 UI n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['VitA200000UI'] = data['text'].split('+')[3]

	def check_albendazole_400_mg(self, data):
		''' This function checks if a quantity sent for Albendazole is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[4]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour Albendazole n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Alb'] = data['text'].split('+')[4]

	def check_var2(self, data):
		'''This function checks if a quantity sent for VAR2 is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[5]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour VAR2 n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['Var2'] = data['text'].split('+')[5]

	def check_mnp(self, data):
		'''This function checks if a quantity sent for MNP is valid '''
		expression = r'^([0-9]+)(.[0-9]+)?$'
		if re.search(expression, data['text'].split('+')[6]) is None:
			data['valide'] = False
			data['response'] = "La quantite envoyee pour MNP n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['mnp'] = data['text'].split('+')[6]

	def save_report(self, data):
		''' This function is used to save a well written report '''
		the_saved_report = Report.objects.create(reporter = data['reporter'],cdd = data['CDD'],text = data['text'],date = datetime.now(),the_concerned_date = data['session'].the_concerned_date ,report_type ='SF' )
		
		the_specific_part_of_sms = StockFinal.objects.create(vitA_100000ui = data['VitA100000UI'],vitB_200000ui = data['VitA200000UI'],albendazole = data['Alb'],var2 = data['Var2'],mnp = data['mnp'],report = the_saved_report)

		#Let's update a session
		data['session'].niveau = 3
		data['session'].save()




	def check_report(self, data):
		'''This method is the main checker'''
		print("..........................check_report debut...................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True


		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		#Let's check if the CDD (Centre de distribution) sent is known in the system
		#and that reporter is registered to report for that CDD
		self.check_site_name(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Vit A 100 000 UI sent by the reporter is valid
		self.check_vitA_100000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Vit A 200 000 UI sent by the reporter is valid
		self.check_vitA_200000ui(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of Albendazole sent by the reporter is valid
		self.check_albendazole_400_mg(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of VAR2 sent by the reporter is valid
		self.check_var2(data)
		if not data['valide']:
			return

		#Let's check if the quantity received (in the morning) of MNP sent by the reporter is valid
		self.check_mnp(data)
		if not data['valide']:
			return

		#Let's save the report
		self.save_report(data)
		if not data['valide']:
			return






#-----------------------------------------------------------------------------------------------------------------------------------------





class BeneficiairesControler():

	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data):
			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."

	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[1]

		if data['session'].cdd_name != sent_cdd_name:
			data['valide'] = False
			data['response'] = "Message non enregistre. Vous n avez pas encore termine avec "+data['session'].cdd_name+"."
			return

		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recoding the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[1]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return


	def check_vit_bleu_6_11_mois(self, data):
		''' This function checks if a quantity of beneficiaries between 6 and 11 months is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[2]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[2]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['vit_bleu_6_11_mois'] = data['text'].split('+')[2]


	def check_vit_rouge_12_59_mois(self, data):
		''' This function checks if a quantity of beneficiaries between 12 and 59 months is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[3]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[3]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['vit_rouge_12_59_mois'] = data['text'].split('+')[3]


	def check_deparasitage_12_23_mois(self, data):
		''' This function checks if a quantity of beneficiaries between 12 and 23 months is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[4]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[4]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['deparasitage_12_23_mois'] = data['text'].split('+')[4]


	def check_deparasitage_2_14_ans(self, data):
		''' This function checks if a quantity of beneficiaries between 2 and 14 years is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[5]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[5]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['deparasitage_2_14_ans'] = data['text'].split('+')[5]


	def check_deparasitage_femmes_enceintes(self, data):
		''' This function checks if a quantity of beneficiaries pregnant mothers is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[6]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[6]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['deparasitage_femmes_enceintes'] = data['text'].split('+')[6]


	def check_var2_18_23_mois(self, data):
		''' This function checks if a quantity of beneficiaries between 18 and 23 months for var 2 is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[7]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[7]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['var2_18_23_mois'] = data['text'].split('+')[7]


	def check_mnp_6_23_mois(self, data):
		''' This function checks if a quantity of beneficiaries between 6 and 23 months for mnp is valid '''
		expression = r'^([0-9]+)$'
		if re.search(expression, data['text'].split('+')[8]) is None:
			data['valide'] = False
			data['response'] = "Le nombre de beneficiaires ("+data['text'].split('+')[8]+") n est pas valide. Veuillez reenvoyer le message avec une valeur valide(un nombre seulement)."
		else:
			data['mnp_6_23_mois'] = data['text'].split('+')[8]


	def save_report(self, data):
		''' This function is used to save a well written report '''
		the_saved_report = Report.objects.create(reporter = data['reporter'],cdd = data['CDD'],text = data['text'],date = datetime.now(),the_concerned_date = data['session'].the_concerned_date ,report_type ='B' )
		
		the_specific_part_of_sms = Beneficiaires.objects.create(vit_bleu_6_11_mois = data['vit_bleu_6_11_mois'], vit_rouge_12_59_mois = data['vit_rouge_12_59_mois'], deparasitage_12_23_mois = data['deparasitage_12_23_mois'], deparasitage_2_14_ans = data['deparasitage_2_14_ans'], deparasitage_femme_enceinte = data['deparasitage_femmes_enceintes'], rattrapage_var2_18_23_mois = data['var2_18_23_mois'], mnp_6_23_mois = data['mnp_6_23_mois'], report = the_saved_report)


		#Let's delete a session
		print("data['session'] avant delete")
		print(data['session'])
		print(data['session'].niveau)
		data['session'].delete()
		data['session'].niveau = 0
		print("data['session'] apres delete")
		print(data['session'].niveau)



	def check_report(self, data):
		'''This method is the main checker'''
		print("..........................check_report debut...................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True


		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		#Let's check if the CDD (Centre de distribution) sent is known in the system
		#and that reporter is registered to report for that CDD
		self.check_site_name(data)
		if not data['valide']:
			return

		#Let's check if
		self.check_vit_bleu_6_11_mois(data)
		if not data['valide']:
			return

		#Let's check if
		self.check_vit_rouge_12_59_mois(data)
		if not data['valide']:
			return

		#Let's check if
		self.check_deparasitage_12_23_mois(data)
		if not data['valide']:
			return

		#Let's check if
		self.check_deparasitage_2_14_ans(data)
		if not data['valide']:
			return

		#Let's check if 
		self.check_deparasitage_femmes_enceintes(data)
		if not data['valide']:
			return

		#Let's check if 
		self.check_var2_18_23_mois(data)
		if not data['valide']:
			return

		#Let's check if 
		self.check_mnp_6_23_mois(data)
		if not data['valide']:
			return


		#Let's save the report
		self.save_report(data)
		if not data['valide']:
			return




#-----------------------------------------------------------------------------------------------------------------------------------------




class RuptureStockControler():

	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if (getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data)):
			print("+++++++getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]]++++++")
			print(getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]])
			print("+++++++++++++")
			print("+++++++len(the_sent_data)++++++")
			print(len(the_sent_data))
			print("+++++++++++++")

			print("+++++++getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data)++++++")
			print(getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data))
			print("+++++++++++++")


			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."

	def check_code_medicament(self, data):
		print("====>Debut de check_code_medicament")
		sent_medicament_code = data['text'].split('+')[1]
		the_concerned_medicament = Medicament.objects.filter(code = sent_medicament_code)
		if len(the_concerned_medicament) < 1:
			data['valide'] = False
			data['response'] = "Le medicament de code ("+sent_medicament_code+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_medicament = the_concerned_medicament[0]
		
			#Let's recod the concerned CDD
			data['medicament'] = one_concerned_medicament

			data['medicament_code'] = data['text'].split('+')[2]


	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[2]
		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recod the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[2]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return

	def save_report(self, data):
		''' This function is used to save a well written report '''
		the_saved_report = Report.objects.create(reporter = data['reporter'],cdd = data['CDD'],text = data['text'],date = datetime.now(),report_type ='B' )
		
		the_specific_part_of_sms = RapportRupture.objects.create(medicament = data['medicament'],probleme_regle = False,report = the_saved_report)


	def check_report(self, data):
		'''This method is the main checker'''
		print("..........................check_report debut...................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True


		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		self.check_site_name(data)
		if not data['valide']:
			return

		self.check_code_medicament(data)
		if not data['valide']:
			return

		self.save_report(data)
		if not data['valide']:
			return




#-----------------------------------------------------------------------------------------------------------------------------------------




class FinRuptureStockControler():

	def check_number_of_sent_valous(self, data):
		'''This function checks if the phone user sent the expected number of values'''
		the_sent_data = data['text'].split('+')
		if (getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data)):
			print("+++++++getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]]++++++")
			print(getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]])
			print("+++++++++++++")
			print("+++++++len(the_sent_data)++++++")
			print(len(the_sent_data))
			print("+++++++++++++")

			print("+++++++getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data)++++++")
			print(getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] > len(the_sent_data))
			print("+++++++++++++")


			data['valide'] = False
			data['response'] = "Votre message est incomplet. Veuillez reenvoyer votre message. Merci."
		if getattr(settings,'VARIABLE_NUMBER','')[data['text'].split('+')[0]] < len(the_sent_data):
			data['valide'] = False
			data['response'] = "Vous avez envoye beaucoup de variable. Veuillez reenvoyer votre message. Merci."

	def check_code_medicament(self, data):
		print("====>Debut de check_code_medicament")
		sent_medicament_code = data['text'].split('+')[1]
		the_concerned_medicament = Medicament.objects.filter(code = sent_medicament_code)
		if len(the_concerned_medicament) < 1:
			data['valide'] = False
			data['response'] = "Le medicament de code ("+sent_medicament_code+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_medicament = the_concerned_medicament[0]
		
			#Let's recod the concerned CDD
			data['medicament'] = one_concerned_medicament

			data['medicament_code'] = data['text'].split('+')[2]


	def check_site_name(self, data):
		''' This function checks if:
			1. the CDD sent is known;
			2. the phone number of the reporter is know as a PHONE NUMBER of A REPORTER
			3. that phone number is allowed to report for that CDD. '''
		sent_cdd_name = data['text'].split('+')[2]
		the_concerned_cdd = CentreDeDistribution.objects.filter(name = sent_cdd_name)
		if len(the_concerned_cdd) < 1:
			data['valide'] = False
			data['response'] = "Le centre de distribution ("+sent_cdd_name+") n est pas connu dans notre systeme."
			return
		else:
			one_concerned_cdd = the_concerned_cdd[0]
		
			#Let's recod the concerned CDD
			data['CDD'] = one_concerned_cdd

			data['CDD_name'] = data['text'].split('+')[2]

			the_phone_number = data['phone']
			the_concerned_phone_number = PhoneNumber.objects.filter(phone_number = the_phone_number)
			if len(the_concerned_phone_number) < 1:
				data['valide'] = False
				data['response'] = "Ton numero de telephone n'est pas reconnu dans notre systeme."
				return
			else:
				#The phone number is allowed to report "Le stock en debut de la journee."
				the_concerned_phone_number = the_concerned_phone_number[0]
				the_phone_owner = the_concerned_phone_number.person
				if the_phone_owner == None:
					#If the phone number is not linked to any person
					data['valide'] = False
					data['response'] = "Ton numero de telephone n est enregistre sur aucune personne."
					return
				else:
					the_reporter = Reporter.objects.filter(person = the_phone_owner)
					if len(the_reporter) < 1:
						#If this person is not registered as a reporter
						data['valide'] = False
						data['response'] = "Vous n etes pas reconnu par le system comme rapporteur."
						return
					else:
						the_reporter = the_reporter[0]

						#Let's report the concerned reporter
						data['reporter'] = the_reporter

						#Let's check if he/she is suposed to report for this site 
						reporter_cdd = CentreDeDistributionReporters.objects.filter(reporter = the_reporter, centre_de_distribution = one_concerned_cdd)
						if len(reporter_cdd) < 1:
							data['valide'] = False
							data['response'] = "Vous n etes pas dans la liste des rapporteurs de ce site."
							return

	def save_report(self, data):
		''' This function is used to save a well written report '''

		#Let's get all stockout reports of that CDD
		stockout_reports = Report.objects.filter(cdd = data['CDD'], report_type = 'RS')

		concerned_rupture = RapportRupture.objects.filter(report__in = stockout_reports, medicament = data['medicament'], probleme_regle = False)

		if len(concerned_rupture) < 1:
			data['valide'] = False
			data['response'] = "Il n y a pas de rapport de rupture ouverte pour le medicament de code ("+data['medicament_code']+") sur le CDD ("+data['CDD_name']+") ."
			return
		else:
			one_concerned_rupture = concerned_rupture[0]
			one_concerned_rupture.probleme_regle = True
			one_concerned_rupture.save()




	def check_report(self, data):
		'''This method is the main checker'''
		print("..........................check_report debut...................................")
		print("This is the begining of check_report of the main controler...")
		#Let's split the text and put the result in data object
		data['splited_text'] = data['text'].split('+')

		data['valide'] = True


		#Let's check if the phone user sent a number of values as expected
		self.check_number_of_sent_valous(data)
		if not data['valide']:
			return

		self.check_site_name(data)
		if not data['valide']:
			return

		self.check_code_medicament(data)
		if not data['valide']:
			return

		self.save_report(data)
		if not data['valide']:
			return
