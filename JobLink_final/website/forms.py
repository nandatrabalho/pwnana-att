from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroUsuarioForm(UserCreationForm):
    TIPO_CHOICES = [
        ("candidato", "Quero procurar vagas"),
        ("empresa", "Quero publicar vagas"),
    ]

    email = forms.EmailField(required=True, label="E-mail")
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, widget=forms.RadioSelect, label="Tipo de conta")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "tipo", "password1", "password2"]
        labels = {
            "username": "Nome de usuário",
            "first_name": "Nome",
            "last_name": "Sobrenome",
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        from .models import Empresa
        model = Empresa
        exclude = ["usuario"]


class CandidatoForm(forms.ModelForm):
    class Meta:
        from .models import Candidato
        model = Candidato
        exclude = ["usuario"]
        widgets = {"telefone": forms.TextInput(attrs={"class": "telefone-mask", "placeholder": "(00) 00000-0000"})}


class CandidaturaForm(forms.ModelForm):
    class Meta:
        from .models import Candidatura
        model = Candidatura
        fields = ["mensagem"]
        widgets = {"mensagem": forms.Textarea(attrs={"rows": 5})}


class RecuperarUsuarioForm(forms.Form):
    email = forms.EmailField(label="E-mail cadastrado", help_text="Enviaremos seu nome de usuário para este endereço.")

