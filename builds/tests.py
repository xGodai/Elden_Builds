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
