from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from checkers import StockDebutJourneeControler, StockRecuLeMatinControler, StockFinalControler, BeneficiairesControler, RuptureStockControler, FinRuptureStockControler
import requests
import json
from ssme_activities.models import PhoneNumber, Reporter, NiveauAvancement, CentreDeDistribution, Report, StockDebutJournee
from jsonview.decorators import json_view


@json_view
def send_sms_via_rapidpro(args):
	'''This function is used to send responses to RapidPro'''
	response = {'ok' : args['valide'], 'response' : args['response']}
	print(response)
	return response

def return_to_rapidPro(args):
	pass


def check_prefixe(args):
	'''This function check if the passed object has a valid prefixe.
	If the prefixe is valid, this function determine also the related controler name.
	'''
	if args['text'].split('+')[0] in getattr(settings,'KNOWN_PREFIXES',''):
		args['valide'] = True
		args['controler_name'] = getattr(settings,'KNOWN_PREFIXES','')[args['text'].split('+')[0]]
	else:
		args['valide'] = False
	
def check_level(args):
	''' This function checks if the incoming message is the expected one. '''
	

	the_phone_number_objects = PhoneNumber.objects.filter(phone_number = args['phone'])
	if len(the_phone_number_objects) < 1:
		args['valide'] = False
		print("This phone number is not known.")
		args['response'] = "Votre numero de telephone n est pas enregistre dans le systeme."
		return
	the_phone_number_object = the_phone_number_objects[0]
	the_person_reporting =  the_phone_number_object.person

	the_reporter_object = Reporter.objects.filter(person = the_person_reporting)
	if len(the_reporter_object) < 1:
		args['valide'] = False
		print("This reporter is not known.")
		args['response'] = "Vous n etes pas dans la liste des rapporteurs."
		return

	the_reporter_object = the_reporter_object[0]


	#Let's check his/here level
	niveaux = NiveauAvancement.objects.filter(reporter = the_reporter_object)
	if len(niveaux) < 1:
		#Le message en cours de traitement doit etre le stock du debut de la journee.
		if args['text'].split('+')[0] != 'SDJ':
			#Il/elle envoie un message qu il fallait pas
			print("Message non enregistre. Vous devez d abord envoyer le stock du debut de la journee")
			args['valide'] = False
			args['response'] = "Message non enregistre. Le premier message doit etre le stock du debut de la journee et doit donc commencer par 'SDJ'."
			return
		print("Le message en cours de traitement doit etre le stock du debut de la journee.")
	else:
		#Ce rapporteur est en cours d'execution du flow.
		niveau_object = niveaux[0]
		niveau = niveau_object.niveau
		args['session'] = niveau_object

		#Let s determine the concerned CDD
		the_concerned_cdd = CentreDeDistribution.objects.filter(name = niveau_object.cdd_name)
		if len(the_concerned_cdd) < 1:
			#Cas impossible
			print("Message non enregistre. Le CDD n existe pas.")
			args['valide'] = False
			args['response'] = "Message non enregistre. Exception: Le CDD n existe pas."
			return
		the_concerned_cdd = the_concerned_cdd[0]

		if niveau == 1:
			#The incoming message must be the "stock recu". Started by SR.
			print("The incoming message must be the stock recu. Started by SR")
			#if args['text'].split('+')[0] not in ["SR","sr"]:
			if args['text'].split('+')[0] != 'SR':
				print("Message non enregistre. Le message devrait commencer par SR.")
				args['valide'] = False
				args['response'] = "Message non enregistre. Vous devriez envoyer les quantites recues. Donc un message commencant par 'SR'."
				#!!!!!Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement'
				#correspondant.
				print("#!!!!! A faire. Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement' correspondant")

				#====>Supprimer le niveau et les rapports lies a ce niveau	
				
				'''concerned_reports = Report.objects.filter(reporter = the_reporter_object, cdd = the_concerned_cdd, the_concerned_date = niveau_object.the_concerned_date)
				if len(concerned_reports) > 0:
					for r in concerned_reports:
						if r.report_type == 'SDJ':
							sdj_report = StockDebutJournee.objects.filter(report = r)
							if len(sdj_report) > 0:
								sdj_report = sdj_report[0]
								sdj_report.delete()
							r.delete()
						if r.report_type == 'SR':
							sr_report = StockRecuLeMatin.objects.filter(report = r)
							if len(sr_report) > 0:
								sr_report = sr_report[0]
								sr_report.delete()
							r.delete()
						if r.report_type == 'SF':
							sf_report = StockFinal.objects.filter(report = r)
							if len(sf_report) > 0:
								sf_report = sf_report[0]
								sf_report.delete()
							r.delete()
						if r.report_type == 'B':
							b_report = Beneficiaires.objects.filter(report = r)
							if len(b_report) > 0:
								b_report = b_report[0]
								b_report.delete()
							r.delete()
				niveau_object.delete()'''

				return

		if niveau == 2:
			#The incoming message must be the "stock recu". Started by SR.
			print("The incoming message must be the 'stock final'. Started by SF")
			#if args['text'].split('+')[0] != 'SF':
			if args['text'].split('+')[0].upper() != 'SF':
				print("Message non enregistre. Le message devrait commencer par SF.")
				args['valide'] = False
				args['response'] = "Message non enregistre. Vous devriez envoyer les quantites finales. Donc um message commencant par 'SF'."
				#!!!!!Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement'
				#correspondant.
				print("#!!!!! A faire. Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement' correspondant")
				

				#====>Supprimer le niveau et les rapports lies a ce niveau
				'''concerned_reports = Report.objects.filter(reporter = the_reporter_object, cdd = the_concerned_cdd, the_concerned_date = niveau_object.the_concerned_date)
				if len(concerned_reports) > 0:
					for r in concerned_reports:
						if r.report_type == 'SDJ':
							sdj_report = StockDebutJournee.objects.filter(report = r)
							if len(sdj_report) > 0:
								sdj_report = sdj_report[0]
								sdj_report.delete()
							r.delete()
						if r.report_type == 'SR':
							sr_report = StockRecuLeMatin.objects.filter(report = r)
							if len(sr_report) > 0:
								sr_report = sr_report[0]
								sr_report.delete()
							r.delete()
						if r.report_type == 'SF':
							sf_report = StockFinal.objects.filter(report = r)
							if len(sf_report) > 0:
								sf_report = sf_report[0]
								sf_report.delete()
							r.delete()
						if r.report_type == 'B':
							b_report = Beneficiaires.objects.filter(report = r)
							if len(b_report) > 0:
								b_report = b_report[0]
								b_report.delete()
							r.delete()
				niveau_object.delete()'''

				return
				

		if niveau == 3:
			#The incoming message must be the "Beneficiaires". Started by B.
			print("The incoming message must be the 'Beneficiaires'. Started by B")
			if args['text'].split('+')[0] != 'B':
				print("Message non enregistre. Le message devrait commencer par B.")
				args['valide'] = False
				args['response'] = "Message non enregistre. Vous devriez envoyer le nombre de Beneficiaires. Donc um message commencant par 'B'."
				#!!!!!Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement'
				#correspondant.
				print("#!!!!!====> A faire. Si je parviens pas a lui maitenir sur le meme niveau dans le flow, je doit annuler l objet 'NiveauAvancement' correspondant")

				#====>Supprimer le niveau et les rapports lies a ce niveau
				'''concerned_reports = Report.objects.filter(reporter = the_reporter_object, cdd = the_concerned_cdd, the_concerned_date = niveau_object.the_concerned_date)
				if len(concerned_reports) > 0:
					for r in concerned_reports:
						if r.report_type == 'SDJ':
							sdj_report = StockDebutJournee.objects.filter(report = r)
							if len(sdj_report) > 0:
								sdj_report = sdj_report[0]
								sdj_report.delete()
							r.delete()
						if r.report_type == 'SR':
							sr_report = StockRecuLeMatin.objects.filter(report = r)
							if len(sr_report) > 0:
								sr_report = sr_report[0]
								sr_report.delete()
							r.delete()
						if r.report_type == 'SF':
							sf_report = StockFinal.objects.filter(report = r)
							if len(sf_report) > 0:
								sf_report = sf_report[0]
								sf_report.delete()
							r.delete()
						if r.report_type == 'B':
							b_report = Beneficiaires.objects.filter(report = r)
							if len(b_report) > 0:
								b_report = b_report[0]
								b_report.delete()
							r.delete()
				niveau_object.delete()'''

				return
		print("Ce rapporteur est en cours d'execution du flow.")
	
def erase(args):
	pass

@csrf_exempt
@json_view
def receive_report(request):
	'''This function will receive requests sent by RapidPro when a new sms report is received by RapidPro.
	This function send json data to RapidPro as a response.'''

	#We will put all data sent by RapidPro in this variable
	incoming_data = {}

	#If the report is correct, incoming_data['valide'] will contain 'True'. If not, it will contains False
	#Until we find out it is not correct, let's assume it's correct.
	incoming_data['valide'] = True

	incoming_data['response']="The default response..."

	#Two couples of variable/value are separated by &
	#Let's put couples of variable/value in a list called 'list_of_data'
	list_of_data = request.body.split("&")

	#Let's put all the incoming data in the dictinary 'incoming_datas'
	for i in list_of_data:
		incoming_data[i.split("=")[0]] = i.split("=")[1]
		
	
	"==print(incoming_data['phone'])=="
	print(incoming_data['phone'])
	#IF the message contains only X, the phone user ask for stoping a flow
	if incoming_data['text'].upper() == 'X':
		print("////APRES if incoming_data['text'].upper() == 'X':////")

		print("...incoming_data['phone']...")
		print(incoming_data['phone'])
		#Let's check if the phone number is registered in the system
		the_phone_number_objects = PhoneNumber.objects.filter(phone_number = incoming_data['phone'])
		print(incoming_data['phone'])
		if len(the_phone_number_objects) < 1:
			print("Le numero de telephone en haut n a pas ete trouve.")
			incoming_data['valide'] = False
			incoming_data['response'] = "Votre numero de telephone n est pas enregistre dans le systeme."
			response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
			print(response)
			return response

		the_phone_number_object = the_phone_number_objects[0]
		the_person_reporting =  the_phone_number_object.person

		the_reporter_object = Reporter.objects.filter(person = the_person_reporting)
		if len(the_reporter_object) < 1:
			incoming_data['valide'] = False
			print("This reporter is not known.")
			incoming_data['response'] = "Vous n etes pas dans la liste des rapporteurs."
			response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
			print(response)
			return response

		the_reporter_object = the_reporter_object[0]

		niveaux = NiveauAvancement.objects.filter(reporter = the_reporter_object)
		if len(niveaux) > 0:
			for n in niveaux:
				n.delete()
		incoming_data['valide'] = 'Exit'
		incoming_data['response'] = "Vous avez ressie a annuler la session."
		response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
		print(response)
		return response
	#
	






	#check if an incoming message has a valide prefixe
	check_prefixe(incoming_data)
	if not incoming_data['valide']:#If the prefix is not known, we inform the user and we stop to deal with this message
		incoming_data['response']="Le mot qui commence votre message n est pas connu. Veuiller reenvoyer le message avec le premier mot valide."
		
		response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
		print(response)
		return response





	#Let check the level.
	check_level(incoming_data)
	if not incoming_data['valide']:
		response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
		print(response)
		return response




	#Let's create an instance of the concerned controler
	try:
		related_checker = globals()[incoming_data['controler_name']]()
		print("////globals()[incoming_data['controler_name']]///")
		print(globals()[incoming_data['controler_name']])
	except:
		print("There is an exception due to the controler which doesn't exist...")
		incoming_data['valide'] = False
		incoming_data['response'] = 'There is an exception due to the controler which does not exist'
		response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
		print(response)
		return response

	#Let's call the check_report() function of the object
	related_checker.check_report(incoming_data)
	if not incoming_data['valide']:
		response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
		print(response)
		return response


	incoming_data['response'] = "Votre message est bien recu. Merci."
	response = {'ok' : incoming_data['valide'], 'response' : incoming_data['response']}
	print(response)
	return response
