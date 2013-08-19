from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'report.views.login',  name='main_index'),
    url(r'^logout/$', 'report.views.logout',  name='logout'),
    url(r'^contact/$', TemplateView.as_view(template_name="contact.html"),  name='contact'),
    url(r'^report/daily/$', 'report.views.daily_report',  name='daily_usage_report'),
    url(r'^report/download_csv/$', 'report.views.download_csv', name='download_csv'),
    url(r'^report/download_pdf/$', 'report.views.download_pdf', name='download_pdf'),
)