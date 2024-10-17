from django import forms

TIPO_USUARIOS = (
    ("COORDENACAO", "Coordenacao"),
    ("ADMINISTRAÇÃO", "Administração"),
)


class FormLogin(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome de usuário', 
            'class': 'form-control form'  
        })
    )
    senha = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha', 
            'class': 'form-control form', 
            'id': 'id_password'  
        })
    )


class FormCadastro(forms.Form):
    nome = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control form'})
    )

    sobrenome = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-control form'})
    )
    
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Nome de usuário', 'class': 'form-control form'})
    )
    
    senha = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control form '})
    )
