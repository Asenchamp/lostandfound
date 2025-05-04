from django.contrib.auth.forms import UserCreationForm
from .models import customUser
from django import forms
from base.models import Village,County
from dal import autocomplete

class usecreationForm(UserCreationForm):

    location = forms.ModelChoiceField(
        queryset=County.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='county-autocomplete',
            attrs={
                'data-minimum-input-lenght':2,
                'data-placeholder':'Start typing your county name...',
            }
        ),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = customUser
        fields = ('username','email','phone_number','location')

class userupdateForm(forms.ModelForm):
    class Meta:
        model = customUser
        fields = ('username','email','last_name','first_name','phone_number','location')

    
        
        