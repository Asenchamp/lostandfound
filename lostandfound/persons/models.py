from django.db import models
from useraccounts.models import authority
from base.models import County


# Create your models here.


# -- defining languages spoken by people in the area
class spoken_languages(models.Model):
    spoken_language_name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.spoken_language_name
    
# -- identifying the races of people in the area
class race(models.Model):
    race_name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.race_name
    
# -- identifying unique features people might have
class distinguishing_features(models.Model):
    distinguishing_feature_name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.distinguishing_feature_name
    
# -- describing lost pipo
class missing_person(models.Model):
    mp_name = models.CharField(max_length=25)
    AGERANGECHOICES = {
        "infants" : "0 - 1",
        "toddler" : "2 - 3",
        "childhood" : "4 - 12",
        "teenage" : "13 - 19",
        "in thier 20s" : "20 - 29",
        "in thier 30s" : "30 - 39",
        "in thier 40s" : "40 - 49",
        "Senior" : "50 and above",
    }
    age_range = models.CharField(max_length=15, choices=AGERANGECHOICES)
    #physical description
    height = models.FloatField()
    BODYBUILDCHOICES = {
        "Slender":"slender",
        "Muscular":"muscular",
        "Average":"average"
    }
    body_build = models.CharField(max_length=15, choices=BODYBUILDCHOICES)
    SKINCOLORCHOICES = {
        "Dark":"dark",
        "Chocolate":"chocolate",
        "Lightskin":"lightskin",
        "White":"white"
    }
    skin_color = models.CharField(max_length=15, choices=SKINCOLORCHOICES)
    race = models.ForeignKey(race,on_delete=models.PROTECT)
    spoken_languages = models.ManyToManyField(spoken_languages, through="missing_person_spoken_languages")
    distinguishing_features = models.ManyToManyField(distinguishing_features, through="missing_person_distinguishing_features")
    # end of physical description
    other_descriptions = models.TextField(null=True, blank=True)
    last_seen_location = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)
    last_seen_date = models.DateTimeField()
    authority = models.ForeignKey(authority, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mp_name
    
    def get_location(self):
        if not self.last_seen_location:
            return "Location not set"
        # parish = self.location.parish
        # subcounty = parish.subcounty
        county = self.last_seen_location
        district = county.district
        # return f"{self.location.name}, {parish.name}, {subcounty.name}, {county.name}, {district.name}"
        return f"{self.last_seen_location.name}, {district.name}"  

# -- describes unique features a person could be having
class missing_person_distinguishing_features(models.Model):
    missing_person = models.ForeignKey(missing_person, on_delete=models.CASCADE)
    distinguishing_features = models.ForeignKey(distinguishing_features, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('missing_person','distinguishing_features'),)

    def __str__(self):
        return self.distinguishing_features.distinguishing_feature_name

# -- describes languages the person can speak
class missing_person_spoken_languages(models.Model):
    missing_person = models.ForeignKey(missing_person, on_delete=models.CASCADE)
    spoken_languages = models.ForeignKey(spoken_languages, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('missing_person','spoken_languages'),)

    def __str__(self):
        return self.spoken_languages.spoken_language_name


class missingpersonOutCome(models.Model):
    STATUSCHOICES = [
        ('alive', 'found alive'),
        ('deceased', 'found deceased'),
        ('still_missing','still missing')
    ]
    missingperson = models.OneToOneField(missing_person, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUSCHOICES)
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
