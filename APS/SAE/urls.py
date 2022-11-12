
"""SAE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django import views
from django.contrib import admin
from django.urls import path
from website import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('',views.loginFuncionario,name='loginFuncionario'),
    path('admin', admin.site.urls),
    path('cadastroFuncionario',views.cadastroFuncionario,name='cadastroFuncionario'),
    path('login',views.loginFuncionario,name='loginFuncionario'),
    path('baixar_arquivo/<str:arquivo>',views.baixar_arquivo, name='baixar_arquivo'),
    path('visualizar_arquivo/<str:arquivo>',views.visualizar_arquivo, name='visualizar_arquivo'),
    path('sair',views.sair),
    path('Dados/<int:id>',views.Dados, name='Dados'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





