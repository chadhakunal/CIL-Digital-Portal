"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cil'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.LogIn.as_view(), name='login'),
    path('adminauth/', views.AdminAuth.as_view(), name='adminauth'),
    path('guestauth/', views.GuestAuth.as_view(), name='guestauth'),
    path('studentauth/', views.StudentAuth.as_view(), name='studentauth'),
    path('guestadd/', views.GuestAdd.as_view(), name='guestadd'),
    path('guestedit/', views.GuestEdit.as_view(), name='guestedit'),
    path('guestupdate/?<int:profile>/', views.GuestUpdate.as_view(), name='guestupdate'),
    path('guestdelete/', views.GuestDelete.as_view(), name='guestdelete'),
    path('logout/', views.logoff, name='logout'),
    path('logsguest/', views.LogGuestView.as_view(), name='logsguest'),
    path('logsstudent/', views.LogStudentView.as_view(), name='logsstudent'),
    path('pastseminars/', views.PastSeminars.as_view(), name='pastseminars'),
    path('seminarreq/', views.SeminarReq.as_view(), name='seminarreq'),
    path('guestsem/', views.GuestUpcomingSeminars.as_view(), name='guestsem'),
    path('admin/logout/', views.logoff, name='adminlogout')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
