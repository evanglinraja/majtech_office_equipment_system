"""
URL configuration for majtech_office_equipment_system project.

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
from category import views as category_view
from equipment import views as equipment_view
from maintenance import views as maintenance_view
from dashboard import views as dashboard_view

urlpatterns = [
    path('', dashboard_view.index),
    path('category', category_view.index),
    path('category/add', category_view.add),
    path('category/edit/<int:id>', category_view.edit),
    path('category/delete/<int:id>', category_view.delete),
    path('equipment', equipment_view.index),
    path('equipment/add', equipment_view.add),
    path('equipment/edit/<int:id>', equipment_view.edit),
    path('equipment/delete/<int:id>', equipment_view.delete),
    path('maintenance', maintenance_view.index),
    path('maintenance/add', maintenance_view.add),
    path('maintenance/edit/<int:id>', maintenance_view.edit),
    path('maintenance/delete/<int:id>', maintenance_view.delete),
    
]
