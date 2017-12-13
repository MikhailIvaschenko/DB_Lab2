"""lab2_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import Scripts.lab2_django_project.startapp_console.views as views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'MainFormTable/$', views.showMainTable),
    url(r'MainFormTable/SearchMainTable/$', views.showSearchTable),
    url(r'MainFormTable/SearchMainTable/MTComeBack/$', views.showMainTable),
    url(r'MainFormTable/SearchMainTable/ACTDateSearch/$', views.acDateSearch),
    url(r'MainFormTable/SearchMainTable/ACTCurrencySearch/$', views.acCurrencySearch),
    url(r'MainFormTable/SearchMainTable/BRDTPriceFilter/$', views.brdPriceFilter),
    url(r'MainFormTable/SearchMainTable/BRDTOrgSearch/$', views.brdOrgSearch),
    url(r'MainFormTable/SearchMainTable/CATCodeSearch/$', views.caCodeSearch),
    url(r'MainFormTable/SearchMainTable/CATSchemeSearch/$', views.caSchemeSearch),
    url(r'MainFormTable/SearchMainTable/NOMTMUSearch/$', views.nomMUSearch),
    url(r'MainFormTable/SearchMainTable/NOMTFTPhraseSearch/$', views.nomFTPhraseSearch),
    url(r'MainFormTable/SearchMainTable/NOMTFTWordSearch/$', views.nomFTWordSearch),

    url(r'MainFormTable/SearchMainTable/\w\w*/STComeBack/$', views.comeBackToSTwithResult),
    url(r'MainFormTable/MTOperationsButtonPressed/$', views.detectButton),
    url(r'MainFormTable/MTOperationsButtonPressed/CommitEditting/$', views.commitEditting),
    url(r'MainFormTable/MTOperationsButtonPressed/CommitAdding/$', views.commitAdding),
    url(r'', views.redirectToMT),
]
