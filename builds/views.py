from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Build
from django.db.models import Count

# Create your views here.


class BuildListView(ListView):
    model = Build
    template_name = 'builds/build_list.html'  
    context_object_name = 'builds'
    
    def get_queryset(self):
        queryset = Build.objects.all()
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort')

        if category:
            queryset = queryset.filter(category=category)
        if sort == 'popular':
            queryset = queryset.annotate(like_count=Count('liked_by')).order_by('-like_count')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

class BuildDetailView(DetailView):
    model = Build
    template_name = 'builds/build_detail.html'  # <app>/<model>_detail.html

class BuildCreateView(LoginRequiredMixin, CreateView):
    model = Build
    fields = ['title', 'description', 'weapons', 'armor', 'talismans', 'spells', 'image', 'category']
    template_name = 'builds/build_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BuildUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Build
    fields = ['title', 'description', 'weapons', 'armor', 'talismans', 'spells', 'image', 'category']
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


class BuildLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        build = get_object_or_404(Build, pk=pk)
        
        if request.user in build.liked_by.all():
            build.liked_by.remove(request.user)
        else:
            build.liked_by.add(request.user)
        
        return redirect('build-detail', pk=pk)
