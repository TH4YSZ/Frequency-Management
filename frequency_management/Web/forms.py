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

class FormPesquisa(forms.Form):
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite aqui o curso ou a turma',
            'class': 'form-control',
            'id': 'search-input'
        }),
        error_messages={
            'required': 'Este campo é obrigatório.',
            'max_length': 'Máximo de 100 caracteres permitido.'
        }
    )
    
    def clean_search(self):
        search = self.cleaned_data.get('search')
        if not search:
            raise forms.ValidationError('Este campo não pode estar vazio.')
        return search.strip()  # Remove espaços em branco extras