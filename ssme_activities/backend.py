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
	'''This function is used to send an sms via RapidPro'''
	'''phone_number = "tel:"+args['phone']
	sms_to_send = args['response']
	data_to_send = {
  					"urn": [phone_number],
  					"text": sms_to_send,
  					"relayer": 156
					}
	#message_url = 'https://rapidpro.io/api/v1/messages.json'
	message_url = 'https://rapidpro.io/api/v1/messages.json'
	token = getattr(settings,'token')
	response = requests.post(message_url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data_to_send))
	print(args['response'])'''
	

	print("b1")

	'''phone_number = "tel:"+args['phone']
	sms_to_send = args['response']
	data_to_send = {
  					"urns": [phone_number],
  					"text": sms_to_send,
  					"relayer": 156
					}
	#message_url = 'https://rapidpro.io/api/v1/messages.json'
	message_url = 'https://api.rapidpro.io/api/v1/broadcasts.json'
	print("b2")
	token = getattr(settings,'token','')
	print("b3")
	#response = requests.post(message_url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data_to_send))
	print("b4")
	print(args['response'])
	print(response)'''

	return {'ok' : args['valide'], 'response' : args['response']}

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
def receive_report(request):
	'''This function will receive requests sent by RapidPro when a new sms repport is received by RapidPro'''
	incoming_data = {}
	incoming_data['valide'] = True
	incoming_data['response']="The default response..."
	resp = 0
	print("111")
	list_of_data = request.body.split("&")
	for i in list_of_data:
		incoming_data[i.split("=")[0]] = i.split("=")[1]
	print("222")
	






	#IF the message contains only X, the phone user ask for stoping a flow
	print("incoming_data['text'].upper() == 'X'")
	print(incoming_data['text'].upper() == 'X')
	if incoming_data['text'].upper() == 'X':
		the_phone_number_objects = PhoneNumber.objects.filter(phone_number = incoming_data['phone'])
		if len(the_phone_number_objects) < 1:
			incoming_data['valide'] = False
			print("This phone number is not known.")
			incoming_data['response'] = "Votre numero de telephone n est pas enregistre dans le systeme."
			return
		the_phone_number_object = the_phone_number_objects[0]
		the_person_reporting =  the_phone_number_object.person

		the_reporter_object = Reporter.objects.filter(person = the_person_reporting)
		if len(the_reporter_object) < 1:
			incoming_data['valide'] = False
			print("This reporter is not known.")
			incoming_data['response'] = "Vous n etes pas dans la liste des rapporteurs."
			return

		the_reporter_object = the_reporter_object[0]

		niveaux = NiveauAvancement.objects.filter(reporter = the_reporter_object)
		if len(niveaux) > 0:
			for n in niveaux:
				n.delete()
		incoming_data['valide'] = True
		#send_sms_via_rapidpro(incoming_data)
		incoming_data['response'] = "Vous avez ressie a annuler la session."
		send_sms_via_rapidpro(incoming_data)
		resp = 0
		return HttpResponse(resp)
	#
	





	print("a1")
	#check if an incoming message has a valide prefixe
	check_prefixe(incoming_data)
	if not incoming_data['valide']:#If the prefix is not known, we inform the user and we stop to deal with this message
		print("a2")
		incoming_data['response']="Le mot qui commence votre message n est pas connu. Veuiller reenvoyer le message avec le premier mot valide."
		send_sms_via_rapidpro(incoming_data)
		print("a3")
		resp = 0
		return HttpResponse(resp)
	print("333")	





	#Let check the level.
	check_level(incoming_data)
	if not incoming_data['valide']:
		#print("incoming_data['response']====>")
		#print(incoming_data['response'])
		send_sms_via_rapidpro(incoming_data)
		return HttpResponse(resp)



	#Let's create an instance of the concerned controler
	try:
		related_checker = globals()[incoming_data['controler_name']]()
		print("////globals()[incoming_data['controler_name']]///")
		print(globals()[incoming_data['controler_name']])
	except:
		print("There is an exception due to the controler which doesn't exist...")
		resp = 0
		return HttpResponse(resp)
	print("444")
	#Let's call the check_report() function of the object
	related_checker.check_report(incoming_data)
	if not incoming_data['valide']:
		#print("incoming_data['response']====>")
		#print(incoming_data['response'])
		send_sms_via_rapidpro(incoming_data)
		return HttpResponse(resp)


	incoming_data['response'] = "Votre message est bien recu. Merci."
	#print("incoming_data['response']====>")
	#print(incoming_data['response'])
	send_sms_via_rapidpro(incoming_data)
	print("FIN...")
	return HttpResponse(resp)
