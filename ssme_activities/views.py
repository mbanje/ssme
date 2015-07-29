from django.shortcuts import render
#from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from django.shortcuts import render_to_response
from django.template import RequestContext
from ssme_activities.forms import identification, HospitalForm, ReportersCDDFrom, CDDForm, CDSForm

from ssme_activities.models import SuperUser, UserDistrict, UserHopital, UserCDS, CentreDeSante, Hospital, District, Reporter, Person, PhoneNumber, CentreDeDistribution, CentreDeDistributionReporters, Report, StockDebutJournee, StockRecuLeMatin, StockFinal, Beneficiaires
import django_tables2

import xlwt

# Create your views here.


@csrf_exempt
def home(request):
	pass
#	msg = 0
#	if request.body:
#		msg = request.body
#	else:
#		msg = "Muri body ntakiriyo"
#
#	print("===================")
#	print("PROJECT_PATH")
#	print(settings.PROJECT_PATH)
#	print("PROJECT_ROOT")
#	print(settings.PROJECT_ROOT)
#	print("===================")
#	
#	return render_to_response("home.html", locals(), context_instance=RequestContext(request))


def identif(request):
	if request.method == 'POST':
		form = identification(request.POST)
		if form.is_valid(): 
			login = form.cleaned_data['login']
			password = form.cleaned_data['password']
			is_super_user = False
			is_district_user = False
			is_hospital_user = False
			is_cds_user = False

			
			super_user = SuperUser.objects.filter(login = login, password = password)
			if len(super_user) < 1:
				is_super_user = True

			district_user = UserDistrict.objects.filter(login = login, password = password)
			if len(district_user) < 1:
				is_district_user = True

			hospital_user = UserHopital.objects.filter(login = login, password = password)
			if len(hospital_user) < 1:
				is_hospital_user = True

			cds_user = UserCDS.objects.filter(login = login, password = password)
			if len(cds_user) < 1:
				is_cds_user = True
			
			#If the user is a super user
			if super_user and not(district_user or hospital_user or cds_user):
				return render(request, 'ssme/super_user_home.html', locals())
			else:
				#If the user is on the district level
				if district_user and not(super_user or hospital_user or cds_user):
					return render(request, 'ssme/district_home.html', locals())
				else:
					#If the user is on the hospital level
					if hospital_user and not(super_user or district_user or cds_user):
						return render(request, 'ssme/hospital_home.html', locals())
					else:
						if cds_user and not(super_user or district_user or hospital_user):
							return render(request, 'ssme/cds_home.html', locals())
						else:
							if not(super_user or district_user or hospital_user or cds_user):
								error = "You are not known by the system"
								return render(request, 'ssme/error.html', locals())
							else:
								error = "There is more than one account with the same login and password"
								return render(request, 'ssme/error.html', locals())
						
				
			
			return render(request, 'ssme/index.html', locals())
		else:
			form = identification()
			return render(request, 'ssme/index.html', locals())

	else:
		form = identification()

		return render(request, 'ssme/index.html', locals())

def reporters_cdd(request):
	reporters = Person.objects.filter(pk__in=Reporter.objects.all())
	if request.method == 'POST':
		form = ReportersCDDFrom(request.POST)
		if form.is_valid(): 
			person_id = form.cleaned_data['Rapporteur']
			cdd_id = form.cleaned_data['CDD']
			print("==")
			print("person_id")
			print(person_id)
			print("cdd_id")
			print(cdd_id)
			print("==")
			
			if person_id == "-1":
				print("Il n y a pas de personne de cette id.")
				return render(request, 'ssme/reporters_cdd.html', locals())
			if cdd_id == "-1":
				print("Il n y a pas de CDD de cette id.")
				return render(request, 'ssme/reporters_cdd.html', locals())
			
			#Let's determine the concerned person
			the_concerned_person = Person.objects.filter(id = person_id)

			if(len(the_concerned_person) < 1):
				print("Il n y a pas de personne de cette id.")
				return render(request, 'ssme/reporters_cdd.html', locals())

			the_concerned_person = the_concerned_person[0]
			
			#Let's determine the concerned reporter
			the_concerned_reporter = Reporter.objects.filter(person = the_concerned_person)
			if len(the_concerned_reporter) < 1:
				print("Cette personne n'est pas un rapporteur.")
				return render(request, 'ssme/reporters_cdd.html', locals())
			the_concerned_reporter = the_concerned_reporter[0]
			

			
			#Let's determine the concerned CDD
			the_concerned_cdd = CentreDeDistribution.objects.filter(id = cdd_id)
			if len(the_concerned_cdd) < 1:
				print("Ce centre de distribution n'existe pas.")
				return render(request, 'ssme/reporters_cdd.html', locals())
			the_concerned_cdd = the_concerned_cdd[0]

			#Let's check if that reporter is already linked to that CDD
			centre_de_distribution_reporters = CentreDeDistributionReporters.objects.filter(centre_de_distribution = the_concerned_cdd, reporter = the_concerned_reporter)
			if len(centre_de_distribution_reporters) > 0:
				print("Ce rapporteur est deja enregistre sur ce centre de distribution.")
				return render(request, 'ssme/reporters_cdd.html', locals())
			
			centre_de_distribution_reporter = CentreDeDistributionReporters.objects.create(centre_de_distribution = the_concerned_cdd, reporter = the_concerned_reporter)
			centre_de_distribution_reporter.save()
			print("It's ok.")
			
			
	form = ReportersCDDFrom()
	return render(request, 'ssme/reporters_cdd.html', locals())

def cds_show(request):
	all_cds = CentreDeSante.objects.all()
	return render(request, 'ssme/cds_show.html', locals())

def hospitals_show(request):
	all_hospitals = Hospital.objects.all()
	if request.method == 'POST':
		form = HospitalForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			district_id = form.cleaned_data['district']

			district = District.objects.filter(id=district_id)
			if len(district) < 1:
				print("Ce district n'existe pas")
				return render(request, 'ssme/hospitals_show.html', locals())
			else:
				district = district[0]
			hopital = Hospital.objects.filter(name=name)
			if len(hopital) > 0:
				print("Un hopital de ce nom est deja enregistre")
				return render(request, 'ssme/hospitals_show.html', locals())
			new_hospital = Hospital.objects.create(name = name, district = district)
			new_hospital.save()
	else:
		form = HospitalForm()
	return render(request, 'ssme/hospitals_show.html', locals())

def districts_show(request):
	all_districts = District.objects.all()
	return render(request, 'ssme/districts_show.html', locals())



'''def cdd_reports(request):
	
	if request.method == 'POST':
		form = CDDForm(request.POST)
		if form.is_valid():
			id_cdd = form.cleaned_data['CDD']
			if id_cdd == '-1':
				print("Nous allons exporter les rapports de toutes les CDD.")
				all_cdd = CentreDeDistribution.objects.all()
				if len(all_cdd) < 1:
					print("Il n y a aucun CDD.")
				else:
					for cdd_instance in all_cdd:
						its_all_reports = Report.objects.filter(cdd = cdd_instance)
						for single_report in its_all_reports:
							if single_report.report_type == 'SDJ':
								the_last_one = Report.objects.filter(cdd = cdd_instance, the_concerned_date = single_report.the_concerned_date).order_by('-id')[0]
								#Let's get the reports sent for the same CDD on the same date
								the_linked_reports = 
			else:
				print("Nous allons exporter les rapports du CDD specifie")
	else:
		form = CDDForm()
	return render(request, 'ssme/cdd_reports.html', locals())'''

def export_reports(request):
	print("ON ENTRE DANS LA FONCTION QUI EXPORTE")
	if request.method == 'POST':
		form = CDSForm(request.POST)
		if form.is_valid():
			id_cds = form.cleaned_data['CDS']
			if id_cds == '-1':
				#On exporte les rapports de tous les CDS
				print("On exporte les rapports de tous les CDS")
				all_cds = CentreDeSante.objects.all()

				book = xlwt.Workbook(encoding="utf-8")
								
				
				for cds_object in all_cds:
					sheet = book.add_sheet("CDS "+cds_object.name)
					its_all_cdd = CentreDeDistribution.objects.filter(centre_de_sante = cds_object)
					ligne = 0
					for cdd_object in its_all_cdd:
						#extrayons toutes les rapports de type SDJ de ce CDD
						its_all_sdj_reports = Report.objects.filter(cdd = cdd_object, report_type = 'SDJ').order_by("id")
						print("00 its_all_sdj_reports 00")
						print(its_all_sdj_reports)
						list_of_finished_dates = []
						for sdj_object in its_all_sdj_reports:
							print("11 sdj_object 11 ")
							print(sdj_object)
							#En cas de plusieurs rapports sur le SDJ, on suppose que le vrai est le dernier
							if sdj_object.the_concerned_date not in list_of_finished_dates:
								ligne = ligne + 1
								the_last_sdj_report_on_this_date = Report.objects.filter(cdd = cdd_object, report_type = 'SDJ', the_concerned_date = sdj_object.the_concerned_date).order_by('id').reverse()[0]

								print("22 the_last_sdj_report_on_this_date 22")
								print(the_last_sdj_report_on_this_date)

								sheet.write(ligne, 0, the_last_sdj_report_on_this_date.text)

								#if len(the_last_sdj_report_on_this_date) > 0:
								the_last_sdj_report_on_this_date_2 = StockDebutJournee.objects.filter(report = the_last_sdj_report_on_this_date)[0]
	


								print("the_last_sr_report_on_this_date : Avant sa naissance")
								
								the_last_sr_report_on_this_date = Report.objects.filter(cdd = cdd_object, report_type ='SR', the_concerned_date = sdj_object.the_concerned_date).order_by('id').reverse()[0]
								print("the_last_sr_report_on_this_date A:")
								print(the_last_sr_report_on_this_date)
								sheet.write(ligne, 1, the_last_sr_report_on_this_date.text)
								print("the_last_sr_report_on_this_date :")
								#if len(the_last_sr_report_on_this_date) > 0:
								the_last_sr_report_on_this_date_2 = StockRecuLeMatin.objects.filter(report = the_last_sr_report_on_this_date)[0]




								the_last_sf_report_on_this_date = Report.objects.filter(cdd = cdd_object, report_type = 'SF', the_concerned_date = sdj_object.the_concerned_date).order_by('id').reverse()[0]

								sheet.write(ligne, 2, the_last_sf_report_on_this_date.text)

								#if len(the_last_sf_report_on_this_date) > 0:
								the_last_sf_report_on_this_date_2 = StockFinal.objects.filter(report = the_last_sf_report_on_this_date)[0]



								the_last_benefi_report_on_this_date = Report.objects.filter(cdd = cdd_object, report_type = 'B', the_concerned_date = sdj_object.the_concerned_date).order_by('id').reverse()[0]

								sheet.write(ligne, 3, the_last_benefi_report_on_this_date.text)

								#if len(the_last_benefi_report_on_this_date) > 0:
								the_last_benefi_report_on_this_date2 = Beneficiaires.objects.filter(report = the_last_benefi_report_on_this_date)
								
								

								list_of_finished_dates.append(sdj_object.the_concerned_date)
				print("===>Avant save<===")
				book.save("/home/mbanje/Documents/my_developpement_folder/ssme/Exported_reports.xls")	
			else:
				#On export les rapports du CDS selectionne
				print("On export les rapports du CDS selectionne")
	else:
		form = CDSForm()
	print("===Avant de sortir de la fonction qui exporte tous les rapports====")
	return render(request, 'ssme/export_reports.html', locals())			
