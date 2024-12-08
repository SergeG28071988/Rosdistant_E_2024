from django.forms import ModelForm, TextInput, Textarea, DateInput
from .models import Human

class HumanForm(ModelForm):
    class Meta:
        model = Human
        fields = ["surname", "name", "date_birth", "place_residence"]
        widgets = {
            "surname": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            "date_birth": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите дату рождения',
                'type': 'date'  # Указываем тип date для календаря
            }),
            "place_residence": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите место проживания'
            })
        }
