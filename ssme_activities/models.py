from django.db import models

# Create your models here.
class Person(models.Model):
	last_name = models.CharField(max_length=30)
	first_name = models.CharField(max_length=30)
	def __unicode__(self):
		name = self.last_name+' '+self.first_name
		return name

class UserDistrict(models.Model):
	person = models.ForeignKey(Person)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

class UserHopital(models.Model):
	person = models.ForeignKey(Person)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

class UserCDS(models.Model):
	person = models.ForeignKey(Person)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

class District(models.Model):
	name = models.CharField(max_length=50)
	users = models.ManyToManyField(UserDistrict, through='District_user')
	def __unicode__(self):
		return self.name

class Hospital(models.Model):
	name = models.CharField(max_length=50)
	district = models.ForeignKey(District)
	users = models.ManyToManyField(UserHopital, through='Hospital_user')
	def __unicode__(self):
		return self.name

class CentreDeSante(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=10)
	hospital = models.ForeignKey(Hospital)
	users = models.ManyToManyField(UserCDS, through='CentreDeSante_user')
	def __unicode__(self):
		return self.name


class PhoneNumber(models.Model):
	phone_number = models.CharField(max_length=12)
	person = models.ForeignKey(Person)
	def __unicode__(self):
		return self.phone_number

class Reporter(models.Model):
	person = models.ForeignKey(Person)

class NiveauAvancement(models.Model):
	reporter = models.ForeignKey(Reporter)
	niveau = models.IntegerField()
	the_concerned_date = models.DateField(auto_now_add=False, auto_now=False)
	cdd_name = models.CharField(max_length=100)

class SuperUser(models.Model):
	person = models.ForeignKey(Person)
	login = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

class TypeCDD(models.Model):
	designation = models.CharField(max_length=30)
	def __unicode__(self):
		return self.designation

class CentreDeDistribution(models.Model):
	name = models.CharField(max_length=50)
	reporters = models.ManyToManyField(Reporter, through='CentreDeDistributionReporters')
	centre_de_sante = models.ForeignKey(CentreDeSante)
	type_cdd = models.ForeignKey(TypeCDD)
	def __unicode__(self):
		return self.name
	
class CentreDeDistributionReporters(models.Model):
	centre_de_distribution = models.ForeignKey(CentreDeDistribution)
	reporter = models.ForeignKey(Reporter)

class CentreDeSante_user(models.Model):
	cds = models.ForeignKey(CentreDeSante)
	user = models.ForeignKey(UserCDS)

class Hospital_user(models.Model):
	hospital = models.ForeignKey(Hospital)
	user = models.ForeignKey(UserHopital)

class District_user(models.Model):
	district = models.ForeignKey(District)
	user = models.ForeignKey(UserDistrict)


class Report(models.Model):
	reporter = models.ForeignKey(Reporter)
	cdd = models.ForeignKey(CentreDeDistribution)
	text = models.CharField(max_length=200)
	#date de reception du rapport
	date = models.DateTimeField(auto_now_add=True, auto_now=False)
	#The date concerned by the report
	the_concerned_date = models.DateField(auto_now_add=False, auto_now=False)
	report_type = models.CharField(max_length=100)
	def __unicode__(self):
		return self.text

class StockDebutJournee(models.Model):
	code_cds = models.CharField(max_length=100)
	nom_site = models.CharField(max_length=50)
	#date concerne par le rapport
	date = models.DateField(auto_now_add=False, auto_now=False)
	vitA_100000ui = models.IntegerField()
	vitB_200000ui = models.IntegerField()
	albendazole = models.IntegerField()
	var2 = models.IntegerField()
	mnp = models.IntegerField()
	report = models.ForeignKey(Report)

class StockRecuLeMatin(models.Model):
	vitA_100000ui = models.IntegerField()
	vitB_200000ui = models.IntegerField()
	albendazole = models.IntegerField()
	var2 = models.IntegerField()
	mnp = models.IntegerField()
	report = models.ForeignKey(Report)

class StockFinal(models.Model):
	vitA_100000ui = models.IntegerField()
	vitB_200000ui = models.IntegerField()
	albendazole = models.IntegerField()
	var2 = models.IntegerField()
	mnp = models.IntegerField()
	report = models.ForeignKey(Report)

class Beneficiaires(models.Model):
	vit_bleu_6_11_mois = models.IntegerField()
	vit_rouge_12_59_mois = models.IntegerField()
	deparasitage_12_23_mois = models.IntegerField()
	deparasitage_2_14_ans = models.IntegerField()
	deparasitage_femme_enceinte = models.IntegerField()
	rattrapage_var2_18_23_mois = models.IntegerField()
	mnp_6_23_mois = models.IntegerField()
	report = models.ForeignKey(Report)

class Medicament(models.Model):
	designation = models.CharField(max_length=200)
	code =  models.CharField(max_length=200)

class RapportRupture(models.Model):
	medicament = models.ForeignKey(Medicament)
	probleme_regle = models.BooleanField(default=False)
	report = models.ForeignKey(Report)
	
	

