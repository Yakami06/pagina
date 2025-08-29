from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, Http404
from .forms import SignupForm, RegistroObjeto, DependenciaFormSet
from .models import Usuario, Objeto, DependenciaRelacion
from django.views.decorators.csrf import csrf_exempt
import json

def lista_objeto(request):
    objetos = list(Objeto.objects.values('id', 'nombre', 't_objeto', 'estatus', 'descripcion'))
    return JsonResponse({'data': objetos})


def relaciones_objeto(request, id):
    try:
        objeto = Objeto.objects.get(id=id)

        
        llama = Objeto.objects.filter(
            dependencias_hacia__desde=objeto,
            dependencias_hacia__tipo='base'
        ).values('id', 'nombre', 't_objeto', 'estatus')

        
        llamado_por = Objeto.objects.filter(
            dependencias_desde__hacia=objeto,
            dependencias_desde__tipo='referencia'
        ).values('id', 'nombre', 't_objeto', 'estatus')

        return JsonResponse({
            'llama': list(llama),
            'llamado_por': list(llamado_por)
        })

    except Objeto.DoesNotExist:
        raise Http404("Objeto no encontrado")



def registro(request):
    return render(request, 'form1.html')


def inicio(request):
    return render(request, 'form.html')


def home(request):
    return render(request, "tabla.html")



def Signup(request): 
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(usuario.password)
            usuario.save()
            request.session['usuario_id'] = usuario.id  
            return redirect('home') 
    else:
        form = SignupForm()

    return render(request, 'form.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['password']

        try:
            usuario = Usuario.objects.get(usuario=username)
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id  
                return redirect('home')  
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'form1.html')



def Ingreso(request): 
    if request.method == 'POST':
        form = RegistroObjeto(request.POST)
        formset = DependenciaFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            objeto = form.save(commit=False)

            usuario_id = request.session.get('usuario_id')
            if usuario_id:
                try:
                    usuario = Usuario.objects.get(id=usuario_id)
                    objeto.usuario = usuario
                    objeto.save()

                    for f in formset:
                        if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                            objeto_hacia = f.cleaned_data.get('objeto')
                            tipo = f.cleaned_data.get('tipo')
                            if objeto_hacia and tipo:
                                DependenciaRelacion.objects.create(
                                    desde=objeto,
                                    hacia=objeto_hacia,
                                    tipo=tipo
                                )

                    return redirect('home')

                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuario inválido')
            else:
                messages.error(request, 'No has iniciado sesión')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = RegistroObjeto()
        formset = DependenciaFormSet()

    return render(request, 'form2.html', {
        'form': form,
        'formset': formset,
        'es_actualizacion': False,
    })



def obtener_objeto(request, id):
    try:
        objeto = Objeto.objects.get(pk=id)
        return JsonResponse({
            'id': objeto.id,
            'nombre': objeto.nombre,
            't_objeto': objeto.t_objeto,
            'estatus': objeto.estatus,
            'descripcion': objeto.descripcion,
        })
    except Objeto.DoesNotExist:
        return JsonResponse({'error': 'Objeto no encontrado'}, status=404)



def actualizar_objeto(request, id):
    objeto = get_object_or_404(Objeto, pk=id)

    dependencias_existentes = DependenciaRelacion.objects.filter(desde=objeto)
    dependencia_data = [{'objeto': d.hacia.id, 'tipo': d.tipo} for d in dependencias_existentes]

    if request.method == 'POST':
        form = RegistroObjeto(request.POST, instance=objeto)
        formset = DependenciaFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            form.save()

            DependenciaRelacion.objects.filter(desde=objeto).delete()

            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
                    objeto_hacia = f.cleaned_data.get('objeto')
                    tipo = f.cleaned_data.get('tipo')
                    if objeto_hacia and tipo:
                        DependenciaRelacion.objects.create(
                            desde=objeto,
                            hacia=objeto_hacia,
                            tipo=tipo
                        )

            return redirect('home')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = RegistroObjeto(instance=objeto)
        formset = DependenciaFormSet(initial=dependencia_data)

    return render(request, 'form2.html', {
        'form': form,
        'formset': formset,
        'es_actualizacion': True,
    })
