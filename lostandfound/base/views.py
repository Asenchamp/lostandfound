from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.list import ListView
from persons.models import missing_person, authority
from .models import Village, County, Image
from dal import autocomplete
from django.http import JsonResponse
from PIL import Image as PILImage
import io
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField, Q
from base.utils.image_processing import process_image
from base.utils.image_search import match_uploaded_image
import pickle
# Create your views here.


# class landingPage(TemplateView):    
#     template_name = 'base/landing.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         search_query = self.request.POST.get('search', '')
#         age_filter = self.request.GET.get('age_filter', '')
#         body_build_filter = self.request.GET.get('body_build_filter', '')
#         skin_color_filter = self.request.GET.get('skin_color_filter', '')
#         features_filter = self.request.GET.get('features_filter', '')
#         uploaded_img = self.request.FILES.get('search_image')
        
#         missingperson = missing_person.objects.filter(is_deleted = False).prefetch_related('spoken_languages').prefetch_related('distinguishing_features')

#         if self.request.user.is_authenticated and self.request.user.location:
#             user_district = self.request.user.location.district
#             missingperson = missingperson.annotate(
#                 is_user_district = Case(
#                     When(last_seen_location__district = user_district, then=Value(1)),
#                     default=Value(2),
#                     output_field=IntegerField(),
#                 )
#             ).order_by('is_user_district','-created_at')
#         else:
#             missingperson = missingperson.order_by('-created_at')

#         if search_query:
#             missingperson = missingperson.filter(Q(mp_name__icontains = search_query) | Q(height__icontains = search_query) | Q(race__race_name__icontains = search_query) | Q(spoken_languages__spoken_language_name__icontains = search_query) | Q(last_seen_location__name__icontains = search_query))

#         if age_filter:
#             missingperson = missingperson.filter(Q(age_range__icontains = age_filter))

#         if body_build_filter:
#             missingperson = missingperson.filter(Q(body_build__icontains = body_build_filter))

#         if skin_color_filter:
#             missingperson = missingperson.filter(Q(skin_color = skin_color_filter))

#         if features_filter:
#             missingperson = missingperson.filter(Q(distinguishing_features__icontains = features_filter))

#         if uploaded_img:
#             matched_images = match_uploaded_image(uploaded_img)
#             print("Matched Images:", matched_images)  # 👈 log the result

#             matched_ids = [img.entity_id for _, img in matched_images]
#             print("Matched Missing Person IDs:", matched_ids)  # 👈 log this too

#             missingperson = missingperson.filter(id__in=matched_ids)

#         #paginate results
#         paginator = Paginator(missingperson, 10) # 10 per page
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
        
#         context['missingperson'] = page_obj

#         #fetch only the first image for the missing person
#         context['missing_person_images'] = {
#             mp.id: Image.objects.filter(
#                 entity_type = 'missingperson',
#                 entity_id = mp.id
#             ).first() or None for mp in page_obj
#         }

#         return context

class landingPage(View):
    template_name = 'base/landing.html'

    def get(self, request):
        return self.handle_request(request)

    def post(self, request):
        return self.handle_request(request)

    def handle_request(self, request):
        data = request.POST if request.method == 'POST' else request.GET

        search_query = data.get('search', '')
        age_filter = data.get('age_filter', '')
        body_build_filter = data.get('body_build_filter', '')
        skin_color_filter = data.get('skin_color_filter', '')
        features_filter = data.get('features_filter', '')
        uploaded_img = request.FILES.get('search_image')

        missingperson = missing_person.objects.filter(is_deleted=False)\
            .prefetch_related('spoken_languages', 'distinguishing_features')

        # prioritize user's district
        if request.user.is_authenticated and request.user.location:
            user_district = request.user.location.district
            missingperson = missingperson.annotate(
                is_user_district=Case(
                    When(last_seen_location__district=user_district, then=Value(1)),
                    default=Value(2),
                    output_field=IntegerField(),
                )
            ).order_by('is_user_district', '-created_at')
        else:
            missingperson = missingperson.order_by('-created_at')

        # text filters
        if search_query:
            missingperson = missingperson.filter(
                Q(mp_name__icontains=search_query) |
                Q(height__icontains=search_query) |
                Q(race__race_name__icontains=search_query) |
                Q(spoken_languages__spoken_language_name__icontains=search_query) |
                Q(last_seen_location__name__icontains=search_query)
            )

        if age_filter:
            missingperson = missingperson.filter(age_range__icontains=age_filter)
        if body_build_filter:
            missingperson = missingperson.filter(body_build__icontains=body_build_filter)
        if skin_color_filter:
            missingperson = missingperson.filter(skin_color=skin_color_filter)
        if features_filter:
            missingperson = missingperson.filter(distinguishing_features__icontains=features_filter)

        # image match filter
        if uploaded_img:
            print("start image search")
            matched_images = match_uploaded_image(uploaded_img)
            matched_ids = [img.entity_id for _, img in matched_images]
            print("Matched IDs:", matched_ids)
            if matched_ids:
                missingperson = missingperson.filter(id__in=matched_ids)
            else:
                missingperson = missingperson.none()
            print("done with image search")

        paginator = Paginator(missingperson, 10)
        page_number = request.GET.get('page') or request.POST.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'missingperson': page_obj,
            'search_query': search_query,
            'missing_person_images': {
                mp.id: Image.objects.filter(entity_type='missingperson', entity_id=mp.id).first()
                for mp in page_obj
            }
        })


class dashboard(LoginRequiredMixin, ListView):
    model = missing_person
    template_name = 'base/dashboaard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        missingperson = missing_person.objects.filter(authority = authority.objects.filter(user = self.request.user).first() , is_deleted=False).prefetch_related('spoken_languages').prefetch_related('distinguishing_features')

        context['missingperson'] = missingperson
        return context


def get_full_location(request, county_id):
    try:
        # village = Village.objects.get(id=village_id)
        # parish = village.parish
        # subcounty = parish.subcounty
        county = County.objects.get(id=county_id)
        district = county.district
        # location_str = f"{village.name}, {parish.name}, {subcounty.name}, {county.name}, {district.name}"
        location_str = f"{county.name}, {district.name}"
        return JsonResponse({'location': location_str})
    except County.DoesNotExist:
        return JsonResponse({'error': 'County not found'}, status=404)

class CountyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = County.objects.all().select_related('district')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs
    
    def get_result_label(self, item):
        return str(item)
    

# -- mixin to handle images ---
class ImageHandlingMixin:
    def handle_images(self, form, entity__type, entity__id):
        # handle image uploads
        images = self.request.FILES.getlist('images')
        for img in images:
            try:
                #open the image with pillow
                pil_image = PILImage.open(img)
                #save it into bytesio object to convrt to .webp
                img_io = io.BytesIO()
                # convert to webp
                pil_image.save(img_io, format="WEBP", quality=85)
                img_io.seek(0)
                # generate new file name with .webp
                new_filename = f"{os.path.splitext(img.name)[0]}.webp"
                img__path = default_storage.save(f"{entity__type.lower()}_images/{new_filename}", ContentFile(img_io.getvalue()))

                #process image
                face_data, descriptor_data = process_image(pil_image)

                # create the image object
                Image.objects.create(
                    image_path = img__path,
                    face_encoding=face_data,
                    feature_descriptor=descriptor_data,
                    entity_type = entity__type,
                    entity_id = entity__id
                )
                print("saved: ", img__path)
            except Exception as e:
                print(f"Failde to process {img.name}: {str(e)}")

    def images_to_delete(self, form, entity__type, entity__id):
        # handle image deletions
        images_to_delete = self.request.POST.getlist('delete_images')
        for img_id in images_to_delete:
            try:
                img = Image.objects.get(id = img_id, entity_type = entity__type, entity_id = entity__id)
                img.delete()
            except Image.DoesNotExist:
                pass