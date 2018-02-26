from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.views import View

from analytics.models import ClickEvent

from .forms import SubmitUrlForm
from .models import ShrtnURL


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        context = {
            'form': the_form,
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            'form': form,
        }
        template = 'shortener/home.html'
        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj, created = ShrtnURL.objects.get_or_create(url=new_url)
            context = {
                'object': obj,
                'created': created,
            }
            if created:
                template = 'shortener/success.html'
            else:
                template = 'shortener/already-exists.html'

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = ShrtnURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)
