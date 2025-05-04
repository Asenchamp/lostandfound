from django.db import models
import os
from django.conf import settings
from django.core.files.storage import default_storage

class District(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class County(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Subcounty(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Parish(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    subcounty = models.ForeignKey(Subcounty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Village(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Image(models.Model):
    image_path = models.CharField(max_length=255)
    face_encoding = models.BinaryField(null=True, blank=True)
    feature_descriptor = models.BinaryField(null=True, blank=True)
    entity_type = models.CharField(max_length=15)
    entity_id = models.PositiveIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image_path}"
    
    # def delete(self, *args, **kwargs):
    #     #delete file from the filesystem if it exists
    #     file_path = os.path.join(settings.MEDIA_ROOT, self.image_path)
    #     if default_storage.exists(self.image_path):
    #         default_storage.delete(self.image_path)
    #     super().delete(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print(f"Deleting file: {self.image_path}")
        if default_storage.exists(self.image_path):
            default_storage.delete(self.image_path)
        else:
            print("File not found in storage.")
        super().delete(*args, **kwargs)



    