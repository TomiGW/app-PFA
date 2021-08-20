from django.db import models
import datetime
from django.utils import timezone
from datetime import timedelta, date

class Rangos(models.Model): #Modelo para los rangos
	nombre= models.CharField(max_length= 50) 
	pago_por_hora= models.IntegerField()
	descripcion= models.CharField(max_length= 100, blank=True)

	def __str__(self):
		return self.nombre

class Policias(models.Model): #Modelo para los oficiales
	nombre = models.CharField(max_length= 50)
	apellido = models.CharField(max_length= 50)
	rango = models.ForeignKey('Rangos', on_delete=models.CASCADE) # Se tiene que ingresar un rango
	nombre_Discord = models.CharField(max_length= 50)
	nombre_Steam = models.CharField(max_length= 100, blank=True)
	fecha_Iniciado = models.DateTimeField( default= timezone.now) # Fecha que ingresa a la PFA

	def __str__(self):
		return "%s %s " % (self.nombre,self.apellido)

	def dias_PFA(self): # Funcion para obtener los dias de antiguedad
		inicio = self.fecha_Iniciado
		dias = 0
		while inicio < timezone.now():
			inicio = inicio + timedelta(days=1)
			dias += 1
		return dias

class CargaHorarias(models.Model): # Modelo para cargar las horas
	policia = models.ForeignKey('Policias', on_delete=models.CASCADE) # Pide un oficial
	horas_totales= models.TimeField() # Se ingresa las horas totales
	fecha_Carga= models.DateField(default=date.today)
	dinero_Extra = models.IntegerField(blank=True, default=0) 

	def __str__(self):
		return "%s" % (self.policia)

	def pagoPorHora(self): # Funcion para calcular el pago a debitar en funcion a las horas totales cargadas
		pago= self.policia.rango.pago_por_hora
		horas= self.horas_totales
		text= str(horas)
		l = text
		if len(text) <= 7:
			l = text[0:4]
			h = l[0:1]
			m = l[2:4]

		if len(text) > 7 and len(text) < 9:
			l = text[0:5]
			h = l[0:2]
			m = l[3:5]

		if len(text) > 9:
			l = text[8:13]
			h = l[0:2]
			m = l[3:5]

		cuenta = pago*int(h) + (pago*(int(m)/60)) + self.dinero_Extra
		return cuenta