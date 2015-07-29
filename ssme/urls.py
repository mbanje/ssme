from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ssme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', TemplateView.as_view(template_name = 'ssme/landing_page.html'), name="landing_page_template"),
        url(r'^ssme/', include('ssme_activities.urls')),
    url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
urlpatterns += staticfiles_urlpatterns()
