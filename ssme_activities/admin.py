from django.contrib import admin
from ssme_activities.models import District, Hospital, CentreDeSante, Person, PhoneNumber, Reporter, UserCDS, UserHopital, UserDistrict,TypeCDD, CentreDeDistribution, CentreDeDistributionReporters, SuperUser, CentreDeSante_user, Hospital_user, District_user, Report, PhoneNumber, Medicament
# Register your models here.

#class ArticleAdmin(admin.ModelAdmin):

admin.site.register(District)
admin.site.register(Hospital)
admin.site.register(CentreDeSante)
admin.site.register(Person)
#admin.site.register(PhoneNumber)
admin.site.register(Reporter)
admin.site.register(UserCDS)
admin.site.register(UserHopital)
admin.site.register(UserDistrict)
admin.site.register(SuperUser)
admin.site.register(TypeCDD)
admin.site.register(CentreDeDistribution)
admin.site.register(CentreDeDistributionReporters)
admin.site.register(CentreDeSante_user)
admin.site.register(Hospital_user)
admin.site.register(District_user)
admin.site.register(Report)
admin.site.register(PhoneNumber)
admin.site.register(Medicament)


