from typing import Any, cast

from django import forms

from authors.models import Author

from .models import Category, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "category",
            "start_date",
            "deadline",
            "image",
        )

        labels = {
            "title": "Título",
            "description": "Descrição",
            "category": "Categoria",
            "start_date": "Data de Início",
            "deadline": "Prazo de conclusão",
            "image": "Imagem (opcional)",
        }

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título da tarefa"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descrição da tarefa",
                    "rows": 4,
                }
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "deadline": forms.DateTimeInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "image": forms.FileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        category_field = cast(forms.ModelChoiceField, self.fields["category"])
        if self.user is None or not getattr(self.user, "is_authenticated", False):
            category_field.queryset = Category.objects.none()
        else:
            category_field.queryset = Category.objects.filter(author=self.user)

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        title = cleaned_data.get("title")

        author = self.user or getattr(self.instance, "author", None)

        if author and title:
            if Task.objects.filter(title=title, author=author).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Essa tarefa já existe.")

        return cleaned_data

    def save(self, commit: bool = True) -> Task:
        task: Task = super().save(commit=False)
        if getattr(self, "user", None) and not getattr(task, "author", None):
            task.author = cast(Author, self.user)
        if commit:
            task.save()
        return task


class TaskUpdateForm(TaskForm):
    def save(self, commit: bool = True) -> Task:
        task: Task = super().save(commit=False)
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
        widgets = {"name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome da categoria"})}

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        name = cleaned_data.get("name")

        if not name:
            raise forms.ValidationError("O nome da categoria é obrigatório.")

        author = self.user or getattr(self.instance, "author", None) or getattr(self.instance, "author_id", None)
        if not author:
            raise forms.ValidationError("Usuário inválido.")

        if Category.objects.filter(name=name, author=author).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Essa categoria já existe.")

        return cleaned_data

    def save(self, commit: bool = True) -> Category:
        category: Category = super().save(commit=False)
        if getattr(self, "user", None) and not getattr(category, "author", None):
            category.author = cast(Author, self.user)
        if commit:
            category.save()
        return category


class CategoryUpdateForm(CategoryForm):
    def save(self, commit: bool = True) -> Category:
        category: Category = super().save(commit=False)
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
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Título"}),
    )
    start_date_from = forms.DateField(
        required=False,
        label="Data início (de)",
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "De",
                "onfocus": "this.type='date'",
                "onblur": "if(!this.value) this.type='text'",
            }
        ),
    )
    start_date_to = forms.DateField(
        required=False,
        label="Data início (até)",
        widget=forms.DateInput(
            attrs={
                "type": "text",
                "class": "form-control",
                "placeholder": "Até",
                "onfocus": "this.type='date'",
                "onblur": "if(!this.value) this.type='text'",
            }
        ),
    )
    completed = forms.ChoiceField(
        required=False,
        label="Concluída",
        choices=(
            ("", "Todos"),
            ("yes", "Concluídas"),
            ("no", "Não concluídas"),
            ("overdue", "Atrasadas"),
        ),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs) -> None:
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        category_field = cast(forms.ModelChoiceField, self.fields["category"])
        if user and getattr(user, "is_authenticated", False):
            category_field.queryset = Category.objects.filter(author=user)
        else:
            category_field.queryset = Category.objects.none()
