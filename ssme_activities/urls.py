from django.conf.urls import *
from ssme_activities.views import home, identif, cds_show, hospitals_show, districts_show, reporters_cdd, export_reports
from ssme_activities.backend import receive_report

urlpatterns = patterns('',
                       # dashboard view for viewing all poll reports in one place
						url(r'^$', identif, name="identification"),
						url(r'^cds$', cds_show, name="cds_show"),
						url(r'^hospitals$', hospitals_show, name="hospitals_show"),
						url(r'^districts$', districts_show, name="districts_show"),
						url(r'^smsreport$', receive_report, name="receive_report"),		
						url(r'^reporters_cdd$', reporters_cdd, name="reporters_cdd"),
						url(r'^export_reports$', export_reports, name="export_reports"),				
)
