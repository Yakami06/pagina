from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import Usuario, Objeto


class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar contraseña',
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['nombre', 'usuario', 'password']  
        labels = {
            'password': 'Contraseña',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
        
    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario')
        if Usuario.objects.filter(usuario=usuario).exists():
            raise forms.ValidationError("Ya existe un Usuario.")
        return usuario


class RegistroObjeto(forms.ModelForm):
    class Meta:
        model = Objeto
        labels = {
            't_objeto' : 'Tipo de objeto'
        }
        exclude = ['usuario', 'dependencias']


class DependenciaForm(forms.Form):
    objeto = forms.ModelChoiceField(
        queryset=Objeto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        required=False   
    )
    tipo = forms.ChoiceField(
        choices=[('base', 'Base'), ('referencia', 'Referencia')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False   
    )

class BaseDependenciaFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        for form in self.forms:
            objeto = form.cleaned_data.get('objeto')
            tipo = form.cleaned_data.get('tipo')


            if not objeto and not tipo:
                continue

            if (objeto and not tipo) or (tipo and not objeto):
                raise forms.ValidationError('Cada dependencia debe tener objeto y tipo completos.')


DependenciaFormSet = formset_factory(
    DependenciaForm,
    formset=BaseDependenciaFormSet,
    extra=1,
    can_delete=True
)

