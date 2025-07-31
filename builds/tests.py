from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Build, Comment, CommentVote

class CommentTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create a test build
        self.build = Build.objects.create(
            user=self.user1,
            title='Test Build',
            description='A test build for testing',
            weapons='Test Sword',
            armor='Test Armor',
            talismans='Test Talisman',
            spells='Test Spell',
            category='PVE'
        )
        
        self.client = Client()

    def test_comment_creation(self):
        """Test that a logged-in user can create a comment"""
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-create', kwargs={'pk': self.build.pk}),
            {'content': 'This is a test comment'}
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Comment.objects.filter(content='This is a test comment').exists())
        
    def test_comment_update(self):
        """Test that a user can update their own comment"""
        # Create a comment
        comment = Comment.objects.create(
            build=self.build,
            user=self.user2,
            content='Original comment'
        )
        
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-update', kwargs={'pk': comment.pk}),
            {'content': 'Updated comment'}
        )
        
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Updated comment')
        
    def test_comment_delete(self):
        """Test that a user can delete their own comment"""
        comment = Comment.objects.create(
            build=self.build,
            user=self.user2,
            content='Comment to delete'
        )
        
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-delete', kwargs={'pk': comment.pk})
        )
        
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
        
    def test_comment_permission_denied(self):
        """Test that users cannot edit/delete other users' comments"""
        comment = Comment.objects.create(
            build=self.build,
            user=self.user1,
            content='User1 comment'
        )
        
        # Try to edit as user2
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.get(
            reverse('comment-update', kwargs={'pk': comment.pk})
        )
        
        self.assertEqual(response.status_code, 403)  # Forbidden


class CommentVoteTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create a test build
        self.build = Build.objects.create(
            user=self.user1,
            title='Test Build',
            description='A test build for testing',
            weapons='Test Sword',
            armor='Test Armor',
            talismans='Test Talisman',
            spells='Test Spell',
            category='PVE'
        )
        
        # Create a test comment
        self.comment = Comment.objects.create(
            build=self.build,
            user=self.user1,
            content='Test comment for voting'
        )
        
        self.client = Client()

    def test_upvote_comment(self):
        """Test that a user can upvote a comment"""
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'upvote'})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after vote
        self.assertTrue(CommentVote.objects.filter(
            comment=self.comment,
            user=self.user2,
            vote_type='upvote'
        ).exists())
        self.assertEqual(self.comment.total_upvotes(), 1)
        self.assertEqual(self.comment.vote_score(), 1)

    def test_downvote_comment(self):
        """Test that a user can downvote a comment"""
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'downvote'})
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after vote
        self.assertTrue(CommentVote.objects.filter(
            comment=self.comment,
            user=self.user2,
            vote_type='downvote'
        ).exists())
        self.assertEqual(self.comment.total_downvotes(), 1)
        self.assertEqual(self.comment.vote_score(), -1)

    def test_change_vote(self):
        """Test that a user can change their vote"""
        self.client.login(username='testuser2', password='testpass123')
        
        # First upvote
        self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'upvote'})
        )
        
        # Then downvote (should change the vote)
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'downvote'})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CommentVote.objects.filter(comment=self.comment, user=self.user2).count(), 1)
        vote = CommentVote.objects.get(comment=self.comment, user=self.user2)
        self.assertEqual(vote.vote_type, 'downvote')
        self.assertEqual(self.comment.vote_score(), -1)

    def test_remove_vote(self):
        """Test that clicking the same vote type removes the vote"""
        self.client.login(username='testuser2', password='testpass123')
        
        # First upvote
        self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'upvote'})
        )
        
        # Upvote again (should remove the vote)
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'upvote'})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CommentVote.objects.filter(comment=self.comment, user=self.user2).exists())
        self.assertEqual(self.comment.vote_score(), 0)

    def test_ajax_vote_response(self):
        """Test that AJAX requests return JSON response"""
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'upvote'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['action'], 'added')
        self.assertEqual(data['upvotes'], 1)
        self.assertEqual(data['score'], 1)

    def test_invalid_vote_type(self):
        """Test that invalid vote types are rejected"""
        self.client.login(username='testuser2', password='testpass123')
        
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': self.comment.pk, 'vote_type': 'invalid'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['error'], 'Invalid vote type')


class BuildSortingTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Create test builds with different timestamps and likes
        from django.utils import timezone
        import datetime
        
        self.build1 = Build.objects.create(
            user=self.user1,
            title='Alpha Build',
            description='First build alphabetically',
            weapons='Sword A',
            armor='Armor A',
            talismans='Talisman A',
            category='PVE'
        )
        
        self.build2 = Build.objects.create(
            user=self.user2,
            title='Beta Build',
            description='Second build alphabetically',
            weapons='Sword B',
            armor='Armor B',
            talismans='Talisman B',
            category='PVP'
        )
        
        self.build3 = Build.objects.create(
            user=self.user1,
            title='Gamma Build',
            description='Third build alphabetically',
            weapons='Sword C',
            armor='Armor C',
            talismans='Talisman C',
            category='BOTH'
        )
        
        # Make build2 more popular (more likes)
        self.build2.liked_by.add(self.user1, self.user2)
        self.build1.liked_by.add(self.user2)
        
        # Add comments to build1 to test comment sorting
        Comment.objects.create(build=self.build1, user=self.user1, content='Comment 1')
        Comment.objects.create(build=self.build1, user=self.user2, content='Comment 2')
        Comment.objects.create(build=self.build2, user=self.user1, content='Comment 3')
        
        self.client = Client()

    def test_sort_by_newest(self):
        """Test sorting builds by newest first (default)"""
        response = self.client.get(reverse('build-list'))
        builds = list(response.context['builds'])
        
        # Should be in reverse chronological order (newest first)
        self.assertEqual(builds[0], self.build3)
        self.assertEqual(builds[1], self.build2)
        self.assertEqual(builds[2], self.build1)

    def test_sort_by_oldest(self):
        """Test sorting builds by oldest first"""
        response = self.client.get(reverse('build-list') + '?sort=oldest')
        builds = list(response.context['builds'])
        
        # Should be in chronological order (oldest first)
        self.assertEqual(builds[0], self.build1)
        self.assertEqual(builds[1], self.build2)
        self.assertEqual(builds[2], self.build3)

    def test_sort_by_popular(self):
        """Test sorting builds by most liked"""
        response = self.client.get(reverse('build-list') + '?sort=popular')
        builds = list(response.context['builds'])
        
        # build2 has 2 likes, build1 has 1 like, build3 has 0 likes
        self.assertEqual(builds[0], self.build2)
        self.assertEqual(builds[1], self.build1)
        self.assertEqual(builds[2], self.build3)

    def test_sort_by_most_commented(self):
        """Test sorting builds by most commented"""
        response = self.client.get(reverse('build-list') + '?sort=most_commented')
        builds = list(response.context['builds'])
        
        # build1 has 2 comments, build2 has 1 comment, build3 has 0 comments
        self.assertEqual(builds[0], self.build1)
        self.assertEqual(builds[1], self.build2)
        self.assertEqual(builds[2], self.build3)

    def test_sort_alphabetically(self):
        """Test sorting builds alphabetically by title"""
        response = self.client.get(reverse('build-list') + '?sort=alphabetical')
        builds = list(response.context['builds'])
        
        # Should be in alphabetical order
        self.assertEqual(builds[0], self.build1)  # Alpha Build
        self.assertEqual(builds[1], self.build2)  # Beta Build
        self.assertEqual(builds[2], self.build3)  # Gamma Build

    def test_filter_by_category(self):
        """Test filtering builds by category"""
        response = self.client.get(reverse('build-list') + '?category=PVE')
        builds = list(response.context['builds'])
        
        # Should only contain PVE builds
        self.assertEqual(len(builds), 1)
        self.assertEqual(builds[0], self.build1)

    def test_combined_filter_and_sort(self):
        """Test combining category filter with sorting"""
        response = self.client.get(reverse('build-list') + '?category=PVP&sort=alphabetical')
        builds = list(response.context['builds'])
        
        # Should only contain PVP builds, sorted alphabetically
        self.assertEqual(len(builds), 1)
        self.assertEqual(builds[0], self.build2)

    def test_context_variables(self):
        """Test that current_sort and current_category are passed to template"""
        response = self.client.get(reverse('build-list') + '?sort=popular&category=PVE')
        
        self.assertEqual(response.context['current_sort'], 'popular')
        self.assertEqual(response.context['current_category'], 'PVE')
