# from django import forms

# TIPO_USUARIOS = (
#     ("COORDENADOR", "Coordenador"),
#     ("PROFESSOR", "Professor"),
# )


# class FormLogin(forms.Form):
#     username = forms.CharField(
#         label="Usuário",
#         max_length=20,
#         widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário', 'class': 'form-control'})
#     )
#     password = forms.CharField(
#         label="Senha",
#         widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'})
#     )


# class FormCadastro(forms.Form):
#     nome = forms.CharField(
#         label="Nome",
#         max_length=20,
#         widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'form-control'}))

#     sobrenome = forms.CharField(
#         label="Sobrenome",
#         max_length=20,
#         widget=forms.TextInput(attrs={'placeholder': 'Sobrenome', 'class': 'form-control'}))

#     username = forms.CharField(
#         label="Usuário",
#         max_length=20,
#         widget=forms.TextInput(attrs={'placeholder': 'Nome de Usuário', 'class': 'form-control'}))

#     senha = forms.CharField(
#         label="Senha",
#         max_length=20,
#         widget=forms.PasswordInput(attrs={'placeholder': 'Senha', 'class': 'form-control'}))