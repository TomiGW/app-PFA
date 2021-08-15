from django.urls import path
from . import views

urlpatterns = [
	path('Home', views.home, name='home'), # url para home

	path('Home/listado', views.listado_policias, name='listaPFA'), #url para ver el listado de policias
	path('Home/listado/nuevo_policia', views.nuevo_policia, name='nuevo_policia'), # url para añadir un nuevo policia
	path('Home/listado/<int:pk>/borrar_policia', views.borrar_policia, name='borrar_policia'), # url para borrar un policia
	path('Home/listado/<int:pk>/editar_policia', views.editar_policia, name='editar_policia'), # url para editar un policia

	path('Informacion', views.cargaHoraria, name='informacion'),
	path('Informacion/<int:pk>/borrar', views.borrar_informacion, name='borrar'), #url para borrar cargas de un oficial
	path('Informacion/borrar_todo', views.borrar_toda_informacion, name='borrar_info'), #url para borrar todas las cargas
	path('Informacion/nueva_carga_horaria', views.nueva_cargaHoraria, name='nueva_cargaHoraria'), #ulr para añadir una nueva carga

	path('Historial_Horas', views.historial_horas, name='historial'), # ulr para ver el historial de cargas 
	path('Historial_Horas/<int:pk>/borrar', views.borrar_hora, name='borrar_hora'), # url para borrar una carga en especifico
	path('Historial_Horas/<int:pk>/editar', views.editar_hora, name='editar_hora') # url para editar una carga en especifico
]