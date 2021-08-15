from django import forms

from .models import *

class CargaHorariaForm(forms.ModelForm):
	class Meta:
		model= CargaHorarias
		fields= ('policia', 'horas_totales', 'dinero_Extra')

class RangoForm(forms.ModelForm):
	class Meta:
		model= Rangos
		fields= ('nombre','pago_por_hora' ,'descripcion')


class OficialForm(forms.ModelForm):
	class Meta:
		model= Policias
		fields= ('nombre', 'apellido', 'rango', 'nombre_Discord', 'nombre_Steam', 'fecha_Iniciado')

