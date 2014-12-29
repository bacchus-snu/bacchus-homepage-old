from django.conf.urls import patterns, include, url
from homepage.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', home),
	(r'^home/$', home),
	(r'^home/(\d+)/$', home_pagination_view),
	(r'^notice/$', notice_view),
	(r'^notice/(\d+)/$', notice_pagination_view),
	(r'^about/$', about),
	(r'^services/terms/$', service_term),
	(r'^services/account/$', service_account),
	(r'^services/server/$', service_server),
	(r'^services/lab/$', service_lab),
	(r'^services/printer/$', service_printer),
	(r'^services/community/$', service_community),
	(r'^faq/$', faq_view),
	(r'^faq/(\d+)/$', faq_pagination_view),
	(r'^qna/server/$', qna_server_view),
	(r'^qna/server/(\d+)/$', qna_server_pagination_view),
	(r'^qna/lab/$', qna_lab_view),
	(r'^qna/lab/(\d+)/$', qna_lab_pagination_view),
	(r'^qna/printer/$', qna_printer_view),
	(r'^qna/printer/(\d+)/$', qna_printer_pagination_view),
	(r'^qna/account/$', qna_account_view),
	(r'^qna/account/(\d+)/$', qna_account_pagination_view),
	(r'^login/$', login_view),
	(r'^logout/$', logout_view),
	(r'^board/show/(\d+)/$', article_show),
	(r'^board/remove/(\d+)/$', article_remove),
	(r'^board/([A-Za-z0-9_]+)/$', board_list),
	(r'^board/([A-Za-z0-9_]+)/(\d+)/$', board_list),
	(r'^board/([A-Za-z0-9_]+)/write/$', board_write),
	(r'^application/program/$', application_program_view),
	(r'^application/program/(\d+)/$', application_program_pagination_view),
    # Examples:
    # url(r'^$', 'bacchus.views.home', name='home'),
    # url(r'^bacchus/', include('bacchus.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
