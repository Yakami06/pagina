from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
from django.contrib.auth.hashers import make_password, is_password_usable

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    usuario = models.CharField(max_length=10)
    rol = models.CharField(max_length=10, blank=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        
        if not is_password_usable(self.password) or not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    TIPO_OBJETO_OPCIONES = [
        ('Tabla', 'Tabla SQL'),
        ('Vista', 'Vista'),
        ('Funcion', 'Función'),
        ('Store procedure', 'Store Procedure'),
        ('Trigger', 'Trigger'),
        ('Job', 'JOB'),
    ]

    ESTATUS_OPCIONES = [
        ('Activo', 'Activo'),
        ('Desactivandose', 'Desactivandose'),
        ('Inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=50)
    t_objeto = models.CharField(max_length=20, choices=TIPO_OBJETO_OPCIONES)
    f_creacion = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=14, choices=ESTATUS_OPCIONES)
    descripcion = models.TextField(blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='objetos')

    dependencias = models.ManyToManyField(
        'self',
        through='DependenciaRelacion',
        symmetrical=False,
        related_name='referenciado_por',
        blank=True
    )

    def __str__(self):
        return self.nombre

class DependenciaRelacion(models.Model):
    TIPO_DEPENDENCIA = [
        ('base', 'Base'),
        ('referencia', 'Referencia'),
    ]

    desde = models.ForeignKey('Objeto', on_delete=models.CASCADE, related_name='dependencias_desde')
    hacia = models.ForeignKey('Objeto', on_delete=models.CASCADE, related_name='dependencias_hacia')
    tipo = models.CharField(max_length=10, choices=TIPO_DEPENDENCIA)

    def __str__(self):
        return f"{self.desde} -> {self.hacia} ({self.tipo})"
