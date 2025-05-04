from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.


class missingpersonAdmin(admin.ModelAdmin):
    model = models.missing_person
    filter_horizontal = ()

    list_display = ('mp_name','age_range','height','body_build','skin_color',
                  'last_seen_location','last_seen_date','authority','get_spoken_languages','get_distinguishing_features','created_at','updated_at')
    
    list_filter = ('age_range','skin_color','body_build','last_seen_date','authority','created_at',
                   'spoken_languages','distinguishing_features','last_seen_location')
    
    search_fields = ('mp_name','age_range','height','skin_color','body_build','last_seen_date','authority','created_at',
                    'other_descriptions','spoken_languages','distinguishing_features','last_seen_location')

    #  get the spoken languages
    def get_spoken_languages(self, obj):
        return ", ".join([lang.spoken_language_name for lang in obj.spoken_languages.all()])
    get_spoken_languages.short_description = 'Spoken Languages'

    # get the distinguishing features
    def get_distinguishing_features(self, obj):
        return ", ".join([feature.distinguishing_feature_name for feature in obj.distinguishing_features.all()])
    get_distinguishing_features.short_description = 'Distinguishing Features'

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_delete_permission(self, request, obj = None):
        return False

    # make sure the admin cant do nothing to the data
    def get_readonly_fields(self, request, obj = ...):        
        #gets all of the field names defined in the model and make them readonly
        readonly = [field.name for field in self.model._meta.fields]
        return readonly
    
    
admin.site.register(models.missing_person,missingpersonAdmin)
admin.site.register(models.distinguishing_features)
admin.site.register(models.spoken_languages)
admin.site.register(models.race)

