from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import Village, County

# Create your models here

# -- creating a custom user
class customUser(AbstractUser):
    #inherits the abstract user and adds more fields
    phone_number = models.CharField(max_length=13, unique=True)
    # location = models.CharField(max_length=40)
    location = models.ForeignKey(County, null=True, blank=True, on_delete=models.SET_NULL)

    def get_location(self):
        if not self.location:
            return "Location not set"
        # parish = self.location.parish
        # subcounty = parish.subcounty
        county = self.location
        district = county.district
        # return f"{self.location.name}, {parish.name}, {subcounty.name}, {county.name}, {district.name}"
        return f"{self.location.name}, {district.name}"    

    def __str__(self):
        return self.username
    
    def is_authority(self):
        return authority.objects.filter(user=self).exists()
    
    def get_authority_type(self):
        authority_record = authority.objects.filter(user=self).first()
        return authority_record.authority_type if authority_record else None   

    def get_authority_id(self):
        authority_id = authority.objects.filter(user=self).first()
        return authority_id.id if authority_id else None

        
# -- categorising authorities
class authority_type(models.Model):
    authority_type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.authority_type_name
    
# -- advancing a user to authority status
class authority(models.Model):
    user = models.ForeignKey(customUser, on_delete=models.CASCADE)
    authority_type = models.ForeignKey(authority_type, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username