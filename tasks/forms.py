from django import forms

from .models import Category, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "category",
            "start_date",
            "image",
        )

        labels = {
            "title": "Título",
            "description": "Descrição",
            "category": "Categoria",
            "start_date": "Data de Início",
            "image": "Imagem (opcional)",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Título da tarefa"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição da tarefa",
                    "rows": 4,
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control-file", "accept": "image/*"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user is None or not getattr(self.user, "is_authenticated", False):
            self.fields["category"].queryset = Category.objects.none()
        else:
            self.fields["category"].queryset = Category.objects.filter(author=self.user)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        author = self.user or getattr(self.instance, "author", None)

        if author and title:
            if (
                Task.objects.filter(title=title, author=author)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise forms.ValidationError("Essa tarefa já existe.")

        return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)
        if getattr(self, "user", None) and not getattr(task, "author", None):
            task.author = self.user
        if commit:
            task.save()
        return task


class TaskUpdateForm(TaskForm):
    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
        return task


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {
            "name": "Nome",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome da categoria"}
            )
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if not name:
            raise forms.ValidationError("O nome da categoria é obrigatório.")

        author = (
            self.user
            or getattr(self.instance, "author", None)
            or getattr(self.instance, "author_id", None)
        )
        if not author:
            raise forms.ValidationError("Usuário inválido.")

        if (
            Category.objects.filter(name=name, author=author)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Essa categoria já existe.")

        return cleaned_data

    def save(self, commit=True):
        category = super().save(commit=False)
        if getattr(self, "user", None) and not getattr(category, "author", None):
            category.author = self.user
        if commit:
            category.save()
        return category


class CategoryUpdateForm(CategoryForm):
    def save(self, commit=True):
        category = super().save(commit=False)
        if commit:
            category.save()
        return category


class TaskFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        label="Categoria",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    title = forms.CharField(
        required=False,
        label="Título",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Título"}
        ),
    )
    start_date_from = forms.DateField(
        required=False,
        label="Data início (de)",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    start_date_to = forms.DateField(
        required=False,
        label="Data início (até)",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    completed = forms.ChoiceField(
        required=False,
        label="Concluída",
        choices=(("", "Todos"), ("yes", "Concluídas"), ("no", "Não concluídas")),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user and getattr(user, "is_authenticated", False):
            self.fields["category"].queryset = Category.objects.filter(author=user)
        else:
            self.fields["category"].queryset = Category.objects.none()
