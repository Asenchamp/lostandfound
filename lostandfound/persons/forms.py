from django import forms
from.models import missing_person,distinguishing_features,spoken_languages, missingpersonOutCome
from base.models import County
from dal import autocomplete

class missingpersonForm(forms.ModelForm):
    spoken_languages = forms.ModelMultipleChoiceField(
        queryset=spoken_languages.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple
    )
    distinguishing_features = forms.ModelMultipleChoiceField(
        queryset=distinguishing_features.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    last_seen_location = forms.ModelChoiceField(
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
    last_seen_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    # images = forms.FileField(required=False, label="Images")

    class Meta:
        model = missing_person
        fields = ['mp_name','age_range','height','body_build','skin_color',
                  'race','other_descriptions','last_seen_location','last_seen_date']
        

class missingpersonOutComeForm(forms.ModelForm):
    class Meta:
        model = missingpersonOutCome
        fields = ['status','notes']








