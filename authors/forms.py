from django import forms

from .models import Author


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("username", "email", "image_profile", "password")
        labels = {
            "username": "Nome de Usuário",
            "email": "E-mail",
            "image_profile": "Imagem de Perfil (Opcional)",
            "password": "Senha",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Seu nome de usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Digite seu e-mail"}
            ),
            "image_profile": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Selecione sua imagem de perfil",
                }
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "Crie sua senha"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not username or not email or not password:
            raise forms.ValidationError("Todos os campos são obrigatórios.")

        elif len(password) < 8:
            raise forms.ValidationError("A senha deve conter pelo menos 8 caracteres.")

        elif Author.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Esse e-mail já está em uso.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class UpdateRegisterForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("username", "email", "image_profile")
        labels = {
            "username": "Nome de Usuário",
            "email": "E-mail",
            "image_profile": "Imagem de Perfil",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Seu nome de usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Digite seu e-mail"}
            ),
            "image_profile": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Selecione sua imagem de perfil",
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
