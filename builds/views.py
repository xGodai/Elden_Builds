from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db import transaction
from .models import Build, BuildImage, Comment, CommentVote
from .forms import BuildForm, BuildImageFormSet, CommentForm
from django.db.models import Count, Q, F
from django.contrib import messages
from users.notifications import NotificationService

# Create your views here.


class BuildListView(ListView):
    model = Build
    template_name = 'builds/build_list.html'
    context_object_name = 'builds'

    def get_queryset(self):
        queryset = Build.objects.all()
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort', 'newest')

        # Apply search filter
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(weapons__icontains=search) |
                Q(armor__icontains=search) |
                Q(talismans__icontains=search) |
                Q(spells__icontains=search) |
                Q(user__username__icontains=search)
            )

        # Apply category filter
        if category:
            queryset = queryset.filter(category=category)

        # Apply sorting
        if sort == 'popular':
            queryset = queryset.annotate(
                like_count=Count('liked_by')
            ).order_by('-like_count', '-created_at')
        elif sort == 'oldest':
            queryset = queryset.order_by('created_at')
        elif sort == 'most_commented':
            queryset = queryset.annotate(
                comment_count=Count('comments')
            ).order_by('-comment_count', '-created_at')
        elif sort == 'alphabetical':
            queryset = queryset.order_by('title')
        else:  # newest (default)
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search'] = self.request.GET.get('search', '')

        # Add user_has_liked information for authenticated users
        if self.request.user.is_authenticated:
            builds = context['builds']
            user_liked_builds = set(
                self.request.user.liked_builds.values_list('id', flat=True)
            )
            for build in builds:
                build.user_has_liked = build.id in user_liked_builds

        return context


class BuildDetailView(DetailView):
    model = Build
    template_name = 'builds/build_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get sort parameter
        sort = self.request.GET.get('comment_sort', 'newest')

        # Get comments with different sorting options
        comments = self.object.comments.all()

        if sort == 'popular':
            # Sort by vote score (upvotes - downvotes)
            comments = comments.annotate(
                upvote_count=Count(
                    'votes', filter=Q(votes__vote_type='upvote')
                ),
                downvote_count=Count(
                    'votes', filter=Q(votes__vote_type='downvote')
                )
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
                comment.current_user_vote = comment.user_vote(
                    self.request.user
                )

        context['comments'] = comments
        context['comment_form'] = CommentForm()
        context['current_sort'] = sort
        return context


class BuildCreateView(LoginRequiredMixin, CreateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'
    success_url = reverse_lazy('build-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Create formset with POST data
            data['image_formset'] = BuildImageFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=BuildImage.objects.none()
            )
        else:
            # Create empty formset for GET requests
            data['image_formset'] = BuildImageFormSet(
                queryset=BuildImage.objects.none()
            )
        return data

    def form_valid(self, form):
        # Save the main build form first
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            # Handle images if any were uploaded
            context = self.get_context_data()
            image_formset = context['image_formset']

            # Only process images if formset is valid or if it's just empty
            if image_formset.is_valid():
                image_formset.instance = self.object
                image_formset.save()

                # If no primary image is set, make the first one primary
                if (self.object.images.exists() and not
                        self.object.images.filter(is_primary=True).exists()):
                    first_image = self.object.images.first()
                    first_image.is_primary = True
                    first_image.save()

            # Always succeed if the main form is valid - images are optional
            messages.success(self.request, 'Build created successfully!')
            return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class BuildUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Build
    form_class = BuildForm
    template_name = 'builds/build_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['image_formset'] = BuildImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data['image_formset'] = BuildImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        # Save the main build form first
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()

            # Handle images if any were uploaded
            context = self.get_context_data()
            image_formset = context['image_formset']

            # Only process images if formset is valid
            if image_formset.is_valid():
                image_formset.save()

                # Ensure at least one primary image if images exist
                if (self.object.images.exists() and not
                        self.object.images.filter(is_primary=True).exists()):
                    first_image = self.object.images.first()
                    first_image.is_primary = True
                    first_image.save()

            # Always succeed if the main form is valid - images are optional
            messages.success(self.request, 'Build updated successfully!')
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

        # Check if user is already liked the build
        is_liked = request.user in build.liked_by.all()

        if is_liked:
            build.liked_by.remove(request.user)
            action = 'unliked'
        else:
            build.liked_by.add(request.user)
            action = 'liked'
            # Create notification for build like
            NotificationService.create_build_like_notification(
                build, request.user
            )

        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'action': action,
                'total_likes': build.total_likes(),
                'is_liked': not is_liked
            })

        # Redirect for non-AJAX requests
        # Try to redirect back to the referring page, otherwise go to build
        next_url = (request.POST.get('next') or
                    request.META.get('HTTP_REFERER'))
        if next_url:
            return redirect(next_url)
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

            # Create notification for build comment
            NotificationService.create_build_comment_notification(
                build, request.user, comment
            )

            messages.success(
                request, 'Your comment has been added successfully!'
            )
        else:
            messages.error(
                request,
                'There was an error with your comment. Please try again.'
            )

        return redirect('build-detail', pk=pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'builds/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def form_valid(self, form):
        messages.success(
            self.request, 'Your comment has been updated successfully!'
        )
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'builds/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        messages.success(
            self.request, 'Your comment has been deleted successfully!'
        )
        return reverse_lazy(
            'build-detail', kwargs={'pk': self.object.build.pk}
        )


class CommentVoteView(LoginRequiredMixin, View):
    def post(self, request, pk, vote_type):
        comment = get_object_or_404(Comment, pk=pk)

        # Validate vote_type
        if vote_type not in ['upvote', 'downvote']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)

        # Check if user already voted
        try:
            existing_vote = CommentVote.objects.get(
                comment=comment, user=request.user
            )
            if existing_vote.vote_type == vote_type:
                # Remove vote if clicking the same vote type
                existing_vote.delete()
                action = 'removed'
            else:
                # Change vote type
                existing_vote.vote_type = vote_type
                existing_vote.save()
                action = 'changed'
                # Create notification for vote change
                NotificationService.create_comment_vote_notification(
                    comment, request.user, vote_type
                )
        except CommentVote.DoesNotExist:
            # Create new vote
            CommentVote.objects.create(
                comment=comment,
                user=request.user,
                vote_type=vote_type
            )
            action = 'added'
            # Create notification for new vote
            NotificationService.create_comment_vote_notification(
                comment, request.user, vote_type
            )

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
