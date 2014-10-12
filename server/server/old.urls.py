from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'server.views.home', name='home'),
    url(r'^register_form$', 'server.views.registerForm', name='registerForm'), # for registration
    url(r'^doreg$', 'server.views.doReg', name='doReg'),# handler
    url(r'^search_form$', 'server.views.searchForm', name='searchForm'),# for searching
    url(r'^search$', 'server.views.search', name='search'), # handler
    url(r'^re_form$', 'server.views.requestForm', name='re_form'), # request form
    url(r'^re_handler$', 'server.views.requestHandler', name='re_handler'),# request handler
    url(r'^grant_form$', 'server.views.grantForm', name='grant_form'), # grant form
    url(r'^grant_handler$', 'server.views.grantHandler', name='grant_handler'), # grant handler
    url(r'^list_form$', 'server.views.listRequestsForm', name='list_form'), # list all requests form
    url(r'^list_handler$', 'server.views.listRequests', name='list_handler'), # list handler
    url(r'^mail_form$', 'server.views.mailForm', name='mail_form'), # mail form
    url(r'^send_mail$', 'server.views.sendMail', name='send_mail'), # mail handler
    url(r'^reg$', 'server.views.register_form', name='reg_f'), # user registration form
    url(r'^login_form$', 'server.views.login_form', name='login_form'),# user login form
    url(r'^register$', 'server.views.register', name='reg'), # registration handler
    url(r'^do_login$', 'server.views.login_view', name='log'), # login handler
    url(r'^loggedin$', 'server.views.loggedin', name='loggedin'),# logged in status
    url(r'^logout$', 'server.views.logout', name='logout'), # logout
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
