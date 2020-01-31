from . import views
from django.conf.urls import url


urlpatterns =[
url(r'^$', views.location, name='m'),





url(r'^signin$', views.signin, name='signin'),
url(r'^signup$', views.signup, name='signup'),
url(r'^register$', views.register, name='register'),
url(r'^f$',views.fview,name='fview'),
url(r'^y$',views.task,name='task'),
url(r'^p$',views.pview,name='pview'),
url(r'^r$',views.report,name='report'),
url(r'^d$',views.latlonview,name='latlonview'),
url(r'^search$',views.search,name='search'),
url(r'^usef$',views.usef,name='usef'),
url(r'^req$',views.req,name='req'),
url(r'^datareq$',views.datareq,name='datareq'),
url(r'^clear$',views.clear,name='clear'),
url(r'^dentry$',views.dentry,name='dentry'),
url(r'^lorp$',views.lorp,name='lorp')
]