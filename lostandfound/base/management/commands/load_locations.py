import json
from django.core.management.base import BaseCommand
from base.models import District, County, Subcounty, Parish, Village

class Command(BaseCommand):
    help = 'Load location data from JSON files'

    def handle(self, *args, **options):
        self.load_districts()
        self.load_counties()
        self.load_subcounties()
        self.load_parishes()
        self.load_villages()
        self.stdout.write(self.style.SUCCESS('All location data loaded successfully!'))

    def load_json(self, filename):
        with open(filename, encoding='utf-8') as f:
            return json.load(f)
        
    def load_districts(self):
        data = self.load_json('data/districts.json')
        for item in data:
            District.objects.get_or_create(id=item["id"], defaults={"name": item["name"]})

    def load_counties(self):
        data = self.load_json('data/counties.json')
        for item in data:
            district = District.objects.get(id = item["district"])
            County.objects.get_or_create(id=item["id"], defaults={"name": item["name"], "district": district})
    
    def load_subcounties(self):
        data = self.load_json('data/subcounties.json')
        for item in data:
            county = County.objects.get(id=item["county"])
            Subcounty.objects.get_or_create(id=item["id"], defaults={"name": item["name"], "county": county})
    
    def load_parishes(self):
        data = self.load_json('data/parishes.json')
        for item in data:
            subcounty = Subcounty.objects.get(id=item["subcounty"])
            Parish.objects.get_or_create(id=item["id"], defaults={"name": item["name"], "subcounty": subcounty})
    
    def load_villages(self):
        data  = self.load_json('data/villages.json')
        for item in data:
            parish = Parish.objects.get(id=item["parish"])
            Village.objects.get_or_create(id=item["id"], defaults={"name": item["name"], "parish": parish})




        