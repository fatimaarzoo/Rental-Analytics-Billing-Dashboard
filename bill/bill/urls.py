"""
URL configuration for bill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main.views import *
from analysis.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home , name= 'home' ),
    path('createbill/', create_bill , name= 'create_bill' ),
    path('addtenant/', addtenant , name= 'addtenant' ),
    path('update-tenant/<id>/', update_tenant , name= 'update_tenant' ),
    path('tenants/', alltenants , name= 'alltenants' ),
    path('tenants/detail/<id>/' , detail, name='detail'),
    path('delete/<id>/', delete_tenant, name= 'delete_tenant'),
    path('bills/', all_bills , name= 'all_bills'),#name is probably used for the return redirect
    path('bill/<id>/', view_bill , name= 'view_bill'),
    path('bill-delete/<id>/', delete_bill, name= 'delete_bill'),
    path('statistics/', monthly_rent_graph  , name= 'monthly_rent_graph' ),
    
]
