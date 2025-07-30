from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Build

# Create your views here.


class BuildListView(ListView):
    model = Build
    template_name = 'builds/build_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'builds'
    ordering = ['-created_at']

class BuildDetailView(DetailView):
    model = Build
    template_name = 'builds/build_detail.html'  # <app>/<model>_detail.html

class BuildCreateView(LoginRequiredMixin, CreateView):
    model = Build
    fields = ['title', 'description', 'weapons', 'armor', 'talismans', 'spells', 'image']
    template_name = 'builds/build_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BuildUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Build
    fields = ['title', 'description', 'weapons', 'armor', 'talismans', 'spells', 'image']
    template_name = 'builds/build_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        build = self.get_object()
        return self.request.user == build.user

class BuildDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Build
    template_name = 'builds/build_confirm_delete.html'
    success_url = reverse_lazy('build-list')

    def test_func(self):
        build = self.get_object()
        return self.request.user == build.user


