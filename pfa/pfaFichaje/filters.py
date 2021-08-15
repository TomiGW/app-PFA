import django_filters
from .models import *

class PoliciaFiltro(django_filters.FilterSet):
	class Meta:
		model= Policias
		fields= ['nombre', 'rango']


class InformacionFiltro(django_filters.FilterSet):
	class Meta:
		model= CargaHorarias
		fields= ['policia' ]