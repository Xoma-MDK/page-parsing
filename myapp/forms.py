from django import forms

class ParseForm(forms.Form):
    SOURCE_CHOICES = [
        ('lenta', 'Lenta.ru'),
        ('rbc', 'RBC.ru'),
    ]
    
    source = forms.ChoiceField(
        choices=SOURCE_CHOICES,
        label='Выберите источник для парсинга',
        initial='lenta'
    )
    parse = forms.CharField(widget=forms.HiddenInput(), initial='parse')