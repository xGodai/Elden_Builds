from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Build, Comment, CommentVote
from .forms import CommentForm
from django.db.models import Count, Q, F
from django.contrib import messages

# Create your views here.


class BuildListView(ListView):
    model = Build
    template_name = 'builds/build_list.html'  
    context_object_name = 'builds'
    
    def get_queryset(self):
        queryset = Build.objects.all()
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort', 'newest')

        if category:
            queryset = queryset.filter(category=category)
            
        if sort == 'popular':
            queryset = queryset.annotate(like_count=Count('liked_by')).order_by('-like_count', '-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'most_commented':
            queryset = queryset.annotate(comment_count=Count('comments')).order_by('-comment_count', '-created_at')
        elif sort == 'alphabetical':
            queryset = queryset.order_by('title')
        else:  # newest (default)
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['current_category'] = self.request.GET.get('category', '')
        return context

class BuildDetailView(DetailView):
    model = Build
    template_name = 'builds/build_detail.html'  # <app>/<model>_detail.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get sort parameter
        sort = self.request.GET.get('comment_sort', 'newest')
        
        # Get comments with different sorting options
        comments = self.object.comments.all()
        
        if sort == 'popular':
            # Sort by vote score (upvotes - downvotes)
            comments = comments.annotate(
                upvote_count=Count('votes', filter=Q(votes__vote_type='upvote')),
                downvote_count=Count('votes', filter=Q(votes__vote_type='downvote'))
            ).annotate(
                vote_score=F('upvote_count') - F('downvote_count')
            ).order_by('-vote_score', '-created_at')
        elif sort == 'oldest':
            comments = comments.order_by('created_at')
        else:  # newest (default)
            comments = comments.order_by('-created_at')
        
        # Add user vote information to each comment
        if self.request.user.is_authenticated:
            for comment in comments:
                comment.current_user_vote = comment.user_vote(self.request.user)
        
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['current_sort'] = sort
        return context

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


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        build = get_object_or_404(Build, pk=pk)
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.build = build
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'There was an error with your comment. Please try again.')
        
        return redirect('build-detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'builds/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'builds/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        messages.success(self.request, 'Your comment has been deleted successfully!')
        return reverse_lazy('build-detail', kwargs={'pk': self.object.build.pk})


class CommentVoteView(LoginRequiredMixin, View):
    def post(self, request, pk, vote_type):
        comment = get_object_or_404(Comment, pk=pk)
        
        # Validate vote_type
        if vote_type not in ['upvote', 'downvote']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)
        
        # Check if user already voted
        try:
            existing_vote = CommentVote.objects.get(comment=comment, user=request.user)
            if existing_vote.vote_type == vote_type:
                # Remove vote if clicking the same vote type
                existing_vote.delete()
                action = 'removed'
            else:
                # Change vote type
                existing_vote.vote_type = vote_type
                existing_vote.save()
                action = 'changed'
        except CommentVote.DoesNotExist:
            # Create new vote
            CommentVote.objects.create(
                comment=comment,
                user=request.user,
                vote_type=vote_type
            )
            action = 'added'
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'action': action,
                'upvotes': comment.total_upvotes(),
                'downvotes': comment.total_downvotes(),
                'score': comment.vote_score(),
                'user_vote': comment.user_vote(request.user)
            })
        
        # Redirect for non-AJAX requests
        return redirect('build-detail', pk=comment.build.pk)
