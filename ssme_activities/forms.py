#-*- coding: utf-8 -*-
from django import forms
from ssme_activities.models import Hospital, District, Reporter, Person, CentreDeDistribution, CentreDeSante


class identification(forms.Form):
	login = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)


class HospitalForm(forms.Form):
	districts = District.objects.all()
	district_list = []
	district_list.append((-1," "))
	for district in districts:
		district_id = district.id
		district_name = district.name
		district_list.append((district_id,district_name))


	name = forms.CharField(max_length=100)
	district = forms.ChoiceField(district_list)
	
	
class ReportersCDDFrom(forms.Form):
	r = Reporter.objects.all()
	reporters = Person.objects.filter(pk__in = Reporter.objects.all())
	#reporters = Person.objects.filter(pk__in = [1,2])
	list_of_all_reporters = []
	list_of_all_reporters.append((-1,""))
	for reporter in reporters:
		person_id = reporter.id
		person_name = reporter.last_name+" "+reporter.first_name
		list_of_all_reporters.append((person_id,person_name))
	
	cdds = CentreDeDistribution.objects.all()
	list_of_cdd = []
	list_of_cdd.append((-1,""))
	for cdd in cdds:
		cdd_name = cdd.name
		cdd_id = cdd.id
		list_of_cdd.append((cdd_id,cdd_name))

	Rapporteur = forms.ChoiceField(list_of_all_reporters)
	CDD = forms.ChoiceField(list_of_cdd)

class CDDForm(forms.Form):
	all_cdd = CentreDeDistribution.objects.all()
	list_of_all_cdd = []
	list_of_all_cdd.append((-1,""))
	for cdd in all_cdd:
		cdd_id = cdd.id
		cdd_name = cdd.name
		list_of_all_cdd.append((cdd_id,cdd_name))
	
	CDD = forms.ChoiceField(list_of_all_cdd)

class CDSForm(forms.Form):
	all_cds = CentreDeSante.objects.all()
	list_of_cds = []
	list_of_cds.append((-1,""))
	for cds in all_cds:
		cds_id = cds.id
		cds_name = cds.name
		list_of_cds.append((cds_id,cds_name))
	CDS = forms.ChoiceField(list_of_cds)
