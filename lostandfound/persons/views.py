from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import missing_person, authority, missingpersonOutCome
from .forms import missingpersonForm, missingpersonOutComeForm
from django.urls import reverse_lazy
from base.models import Image
from base. views import ImageHandlingMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from useraccounts.models import customUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives

# Create your views here.

# -- adding a missing personels
class addMissingPerson(LoginRequiredMixin, CreateView, ImageHandlingMixin):
    model = missing_person
    form_class = missingpersonForm
    template_name = 'persons/missing_person_form.html'
    success_url = reverse_lazy('dashboard')

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors.as_json())
        return super().form_invalid(form)

    def form_valid(self, form):
        # auto assig the missing person to the logged in user authority
        form.instance.authority = authority.objects.get(user=self.request.user)
        response = super().form_valid(form) # save the person first
        #set spoken_languages many to many field
        form.instance.spoken_languages.set(form.cleaned_data.get('spoken_languages'))
        # set distinguishing_features many to many field
        form.instance.distinguishing_features.set(form.cleaned_data.get('distinguishing_features'))
        #handle images with the mixin
        self.handle_images(form, 'missingperson', self.object.id)
        
        #notify users nearby
        mp_location = self.object.last_seen_location
        nearby_users = customUser.objects.filter(location = mp_location).exclude(id=self.request.user.id)
        for user in nearby_users:
            subject = "Missing Person Alert in Your Area"
            html_content = render_to_string('emails/missing_person_alert.html',{
                'person': self.object,
                'url' : f'http://127.0.0.1:8000/persons/detailsMissingPerson/{self.object.id}/',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, text_content, None, [user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()
        
        return response

# --- update details of a missing person
class updateMissingPerson(LoginRequiredMixin, UserPassesTestMixin, UpdateView, ImageHandlingMixin):
    model = missing_person
    form_class = missingpersonForm
    template_name = 'persons/missing_person_form.html'
    success_url = reverse_lazy('dashboard')

    # make sure the person updating is the one who posted
    def test_func(self):
        missingperson = self.get_object()
        return self.request.user == missingperson.authority.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fetch images for the person
        missing_person_images = Image.objects.filter(entity_type="missingperson", entity_id=self.object.id)
        context['missing_person_images'] = missing_person_images
        return context

    def form_valid(self, form):
        #set spoken_languages many to many field
        form.instance.spoken_languages.set(form.cleaned_data.get('spoken_languages'))
        # set distinguishing_features many to many field
        form.instance.distinguishing_features.set(form.cleaned_data.get('distinguishing_features'))
        #handle images with mixin
        print("handling images ")
        self.handle_images(form, 'missingperson', self.object.id)
        print("done handling images")
        self.images_to_delete(form, 'missingperson', self.object.id)

        return super().form_valid(form)


# ---- see more details about the missing person
class detailsMissingPerson(DetailView):
    model = missing_person
    template_name = 'persons/missing_person_details.html'
    context_object_name = 'missingperson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # fetch images for the person
        missing_person_images = Image.objects.filter(entity_type="missingperson", entity_id=self.object.id)
        context['missing_person_images'] = missing_person_images
        return context

# -- delete the missing person 
class deleteMissingPerson(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = missing_person
    template_name = 'persons/missing_person_delete.html'
    success_url = reverse_lazy('dashboard')

    #make sure the person deleting is the one who posted
    def test_func(self):
        missingperson = self.get_object()
        return self.request.user == missingperson.authority.user
    
class ReportOutComeAndDelete(LoginRequiredMixin, FormView):
    template_name = 'persons/missing_person_delete.html'
    form_class = missingpersonOutComeForm

    def dispatch(self, request, *args, **kwargs):
        self.misssing_person = get_object_or_404(missing_person, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        #save the given info
        outcome = form.save(commit = False)
        outcome.missingperson = self.misssing_person
        outcome.save()
        #soft delete person
        self.misssing_person.is_deleted = True
        self.misssing_person.deleted_at = timezone.now()
        self.misssing_person.save()

        return redirect('dashboard')
    


