from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from .filters import *

# VISTAS DEL MENU
def home(request):
	return render(request, 'pfaHtml/home.html', {})

# VISTAS DE LOS POLICIAS (A/B/M)
def listado_policias(request):
	queryset = request.GET.get("buscar") # Obtiene el resultado de la barra de busqueda
	if queryset:
		pfa = Policias.objects.order_by("-rango").filter(Q(nombre__iexact= queryset) | Q(apellido__iexact= queryset)).distinct() #Crea la lista a partir de la barra de busqueda
	else:
		pfa = Policias.objects.order_by("-rango") #Si no se busco nada, se crea la lista con todos lo policias existentes
	

	return render(request, 'pfaHtml/policiaTemplates/policias.html', {'pfa': pfa})

def nuevo_policia(request): #Vista para añadir un policia
	if request.method == "POST":
		form_policia = OficialForm(request.POST)
		if form_policia.is_valid():
			policia = form_policia.save(commit=False)
			policia.save()
			return redirect('nuevo_policia')
	else:
		form_policia= OficialForm()

	return render(request, 'pfaHtml/policiaTemplates/nuevo_policia.html', {'form_policia': form_policia})

def editar_policia(request, pk): # Vista para editar un policia
	policia = get_object_or_404(Policias, pk=pk)
	if request.method == "POST":
		form = OficialForm(request.POST, instance=policia)
		if form.is_valid():
			policia = form.save(commit=False)
			policia.save()
			return redirect('listaPFA')
	else:
		form = OficialForm(instance=policia)
	return render(request, 'pfaHtml/policiaTemplates/editar_policia.html', {'form': form})


def borrar_policia(request, pk): # Vista para borrar un policia
	oficial = get_object_or_404(Policias, pk=pk)
	messages.info(request, 'Se a eliminado el oficial')
	oficial.delete()
	return redirect('listaPFA')



# VISTAS PARA LAS CARGAS DE HORAS (A/B/M)
def cargaHoraria(request): # Muestra las horas cargadas TOTALES de cada oficial
	carga= CargaHorarias.objects.order_by("policia") 
	# Se crean 3 listas para guardar los datos que se necesitan
	oficiales=[]
	montos = []
	tiempo = []
	horas = datetime.timedelta(hours=0, minutes=0) # Se un objeto datetime con valores hora y minutos en 0
	horasT = (00, 00) # Se crea una tupla donde se van a guardar las horas y minutos totales 
	resultado = salario = 0 # Variables donde se setea en 0 el salario de cada objeto y el resultado final donde se guarda la sumatoria de salarios

	for x in carga:
		salario = x.pagoPorHora() #Se obtiene el pago de cada carga
		horas = x.horas_totales # Se obtiene las horas totales de cada carga
		
		if x.policia not in oficiales and len(oficiales) == 0: # Verifica si la carga del oficial se encuentra en la lista correspondiente y si dicha lista esta vacia
			oficiales.append(x.policia) 

		elif x.policia not in oficiales: # Verifica si la carga del oficial se encuentra en la lista correspondiente
			oficiales.append(x.policia)
			montos.append("{0:.2f}".format(resultado))
			tiempo.append(horasT) #Se guardan en las listas que corresponden, el salario final y las horas totales del oficial anterior.
			resultado = 0
			horasT = (00, 00)

		if x.policia in oficiales: # En caso de que el oficial si este en la lista, se hace la sumatoria del salario con el resultado final y lo mismo con las horas
			resultado= resultado + salario 
			horasT = (horas.hour + horasT[0], horas.minute + horasT[1])

	montos.append("{0:.2f}".format(resultado))
	tiempo.append(horasT)

	final = zip(oficiales,montos,tiempo)

	return render(request, 'pfaHtml/horariosTemplates/informacion.html', {'final': final})


def borrar_informacion(request, pk):  #Borrar todas las cargas de un oficial en particular
	filtro = CargaHorarias.objects.filter(policia_id=pk) #La lista generada son apartir del oficial indicado
	for e in filtro: 
		e.delete() # Se borran cada uno de las cargar del oficial
	return redirect('informacion')

def borrar_toda_informacion(request): #Borra todas las cargas de horas que se hayan ingresado
	horas = CargaHorarias.objects.all()
	horas.delete()
	return redirect('informacion')

def historial_horas(request): # Muestra el historial de cargas, en el html solo se muestran las ultimas 15
	carga= CargaHorarias.objects.all()
	return render(request, 'pfaHtml/horariosTemplates/ultimas_cargas_horarias.html', {'carga': carga})

def nueva_cargaHoraria(request): # Añade una nueva carga de horas
	if request.method == "POST":
		form_horario = CargaHorariaForm(request.POST)
		if form_horario.is_valid():
			horario = form_horario.save(commit=False)
			horario.save()
			return redirect('nueva_cargaHoraria')
	else:
		form_horario= CargaHorariaForm()

	return render(request, 'pfaHtml/horariosTemplates/nueva_carga_horaria.html', {'form_horario': form_horario})			

def editar_hora(request, pk): # Edita una carga de horas
	horas = get_object_or_404(CargaHorarias, pk=pk)
	if request.method == "POST":
		form = CargaHorariaForm(request.POST, instance=horas)
		if form.is_valid():
			horas = form.save(commit=False)
			horas.save()
			return redirect('historial')
	else:
		form = CargaHorariaForm(instance=horas)
	return render(request, 'pfaHtml/horariosTemplates/editar_hora.html', {'form': form})

def borrar_hora(request, pk): # Borra una carga de horas en particular
	horas = get_object_or_404(CargaHorarias, pk=pk)
	messages.info(request, 'Se a eliminado esta carga horaria')
	horas.delete()
	return redirect('historial')
