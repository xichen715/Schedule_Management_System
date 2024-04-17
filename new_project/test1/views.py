from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.http import Http404, HttpResponseNotFound
from datetime import datetime, timedelta
import re
import json
from django.http import HttpResponse
from .models import Event, Notebook
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
import datetime
from .forms import EventForm
from . import models
class HomePageView(TemplateView):
    template_name='home.html'
    

class EventView(LoginRequiredMixin, View):
    def get(self, request):
        ret = dict()
        my_event_all = Event.objects.filter(user=request.user)
        ret['my_event_all'] = my_event_all
        return render(request, 'event.html', ret)

class EventInfoView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event_info.html'
    def get_queryset(self):
        return models.Event.objects.filter(start_time__lte=datetime.datetime.now()+datetime.timedelta(days=5), start_time__gte=datetime.datetime.now(), user=self.request.user).order_by('start_time')

class EventCreateView(LoginRequiredMixin, View):

    def get(self, request):
        ret = dict()
        priority_all = [{'key': i[0], 'value': i[1]} for i in Event.priority_choices]
        ret['priority_all'] = priority_all
        if 'calDate' in request.GET and request.GET['calDate']:
            calDate = re.split('[-: ]', request.GET['calDate'])
            Y, M, D, h, m = map(int, calDate)
            start_time = datetime.datetime(Y, M, D, h, m)
            end_time = start_time + timedelta(hours=1)
            ret['start_time'] = start_time
            ret['end_time'] = end_time
        return render(request, 'event_create.html', ret)

    def post(self, request):
        res = dict(result=False)
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')

class EventDetailView(LoginRequiredMixin,View):
    def get(self, request):
        ret = dict()
        if 'id' in request.GET and request.GET['id']:
            priority_all = [{'key': i[0], 'value': i[1]} for i in Event.priority_choices]
            event = get_object_or_404(Event, pk=int(request.GET['id']))
            ret['priority_all'] = priority_all
            ret['event'] = event
        return render(request, 'event_detail.html', ret)

    def post(self, request):
        res = dict(result=False)
        if  'id' in request.POST and request.POST['id']:
            event_detail = get_object_or_404(Event, pk=int(request.POST['id']))
            event_form = EventForm(request.POST, instance=event_detail)
            if event_form.is_valid():
                event_form.save()
                res['result'] = True
        return HttpResponse(json.dumps(res), content_type='application/json')


from django.urls import reverse_lazy
class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('event')

class NotebookListView(LoginRequiredMixin, ListView):
    model = Notebook
    template_name = 'notebook.html'
    paginate_by = 3
    def get_queryset(self):
        return models.Notebook.objects.filter(author=self.request.user).order_by('-create_date')

class NotebookCreateView(LoginRequiredMixin, CreateView):
    model = Notebook
    template_name = 'notebook_create.html'
    fields = [ 'title', 'body','cover']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NotebookDetailView(LoginRequiredMixin, DetailView):
    model = Notebook
    template_name = 'notebook_detail.html'
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return HttpResponseNotFound('<h1>Page not found</h1>')

class NotebookUpdateView(LoginRequiredMixin, UpdateView):
    model = Notebook
    template_name = 'notebook_update.html'
    fields = [ 'title','body','cover']
    
class NotebookDeleteView(DeleteView):
    model = Notebook
    template_name = 'notebook_delete.html'
    success_url = reverse_lazy('notebook')
# Create your views here.






