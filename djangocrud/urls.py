"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from tasks import views 
from tasks.views import lista_objeto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', views.Signup, name='registro'),
    path('home/', views.home, name="home"),  
    path('inicio/', views.login_view, name='inicio'),
    path('', views.login_view, name='login'),
    path('lista_objeto/', lista_objeto, name='lista_objeto'),
    path('nuevo_objeto/', views.Ingreso, name='nuevo_objeto'),
    path('relaciones_objeto/<int:id>', views.relaciones_objeto, name='relaciones_objeto'),
     path('objeto/<int:id>', views.obtener_objeto),
    path('actualizar/<int:id>/', views.actualizar_objeto, name='editar_objeto'),
]

   
    