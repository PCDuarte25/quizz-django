from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class': 'nes-input'})
        self.label_suffix = ''


    class Meta:
        model = Person
        fields = ['name']


