from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from builds.models import Build, Comment, CommentVote
from users.models import Notification, UserProfile
from users.notifications import NotificationService


class NotificationSystemTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
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
        
        # Get the auto-created user profiles and set notification preferences
        self.profile1 = self.user1.profile
        self.profile1.notify_on_build_like = True
        self.profile1.notify_on_build_comment = True
        self.profile1.notify_on_comment_reply = True
        self.profile1.notify_on_comment_vote = True
        self.profile1.save()
        
        self.profile2 = self.user2.profile
        self.profile2.notify_on_build_like = True
        self.profile2.notify_on_build_comment = True
        self.profile2.notify_on_comment_reply = True
        self.profile2.notify_on_comment_vote = True
        self.profile2.save()
        
        # Create a test build
        self.build = Build.objects.create(
            user=self.user1,
            title="Test Build for Notifications",
            description="A test build for notification testing",
            weapons="Test Weapon",
            armor="Test Armor",
            talismans="Test Talisman",
            spells="Test Spell",
            category="PVE"
        )

    def test_build_like_notification_creation(self):
        """Test that liking a build creates a notification"""
        self.client.login(username='testuser2', password='testpass123')
        
        # Like the build
        response = self.client.post(reverse('build-like', kwargs={'pk': self.build.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect after like
        
        # Check if notification was created
        notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='build_like'
        )
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.build, self.build)
        self.assertIn('liked your build', notification.message)

    def test_build_comment_notification_creation(self):
        """Test that commenting on a build creates a notification"""
        self.client.login(username='testuser2', password='testpass123')
        
        # Comment on the build
        comment_data = {
            'content': 'This is a test comment for notifications'
        }
        response = self.client.post(
            reverse('comment-create', kwargs={'pk': self.build.pk}),
            data=comment_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after comment
        
        # Check if notification was created
        notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='build_comment'
        )
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(notification.build, self.build)
        self.assertIn('commented on your build', notification.message)

    def test_comment_vote_notification_creation(self):
        """Test that voting on a comment creates a notification"""
        # Create a comment by user2
        comment = Comment.objects.create(
            build=self.build,
            user=self.user2,
            content="Test comment for voting"
        )
        
        self.client.login(username='testuser1', password='testpass123')
        
        # Upvote the comment
        response = self.client.post(
            reverse('comment-vote', kwargs={'pk': comment.pk, 'vote_type': 'upvote'}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        
        # Check if notification was created
        notifications = Notification.objects.filter(
            recipient=self.user2,
            notification_type='comment_vote'
        )
        self.assertEqual(notifications.count(), 1)
        
        notification = notifications.first()
        self.assertEqual(notification.sender, self.user1)
        self.assertEqual(notification.comment, comment)
        self.assertIn('upvoted your comment', notification.message)

    def test_notification_preferences_respected(self):
        """Test that notification preferences are respected"""
        # Disable build like notifications for user1
        self.profile1.notify_on_build_like = False
        self.profile1.save()
        
        self.client.login(username='testuser2', password='testpass123')
        
        # Like the build
        response = self.client.post(reverse('build-like', kwargs={'pk': self.build.pk}))
        self.assertEqual(response.status_code, 302)
        
        # Check that no notification was created
        notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='build_like'
        )
        self.assertEqual(notifications.count(), 0)

    def test_no_self_notification(self):
        """Test that users don't get notifications for their own actions"""
        self.client.login(username='testuser1', password='testpass123')
        
        # Like own build
        response = self.client.post(reverse('build-like', kwargs={'pk': self.build.pk}))
        self.assertEqual(response.status_code, 302)
        
        # Check that no notification was created
        notifications = Notification.objects.filter(
            recipient=self.user1,
            notification_type='build_like'
        )
        self.assertEqual(notifications.count(), 0)

    def test_notification_list_view(self):
        """Test the notification list view"""
        # Create a test notification
        NotificationService.create_build_like_notification(self.build, self.user2)
        
        self.client.login(username='testuser1', password='testpass123')
        
        # Access notification list
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'liked your build')

    def test_notification_mark_as_read(self):
        """Test marking notifications as read"""
        # Create a test notification
        NotificationService.create_build_like_notification(self.build, self.user2)
        notification = Notification.objects.filter(recipient=self.user1).first()
        self.assertFalse(notification.is_read)
        
        self.client.login(username='testuser1', password='testpass123')
        
        # Mark as read
        response = self.client.post(reverse('notification-mark-read'), {
            'notification_ids': [notification.id]
        })
        self.assertEqual(response.status_code, 200)
        
        # Check if marked as read
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_notification_count_in_context(self):
        """Test that unread notification count is available in context"""
        # Create some test notifications
        NotificationService.create_build_like_notification(self.build, self.user2)
        NotificationService.create_build_comment_notification(
            self.build, 
            self.user2, 
            Comment.objects.create(build=self.build, user=self.user2, content="Test")
        )
        
        self.client.login(username='testuser1', password='testpass123')
        
        # Check any page has the notification count
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # The context should include unread notification count
        self.assertIn('unread_count', response.context)
        self.assertEqual(response.context['unread_count'], 2)

    def test_notification_service_methods(self):
        """Test the NotificationService methods directly"""
        # Test build like notification
        NotificationService.create_build_like_notification(self.build, self.user2)
        self.assertEqual(
            Notification.objects.filter(notification_type='build_like').count(), 
            1
        )
        
        # Test build comment notification
        comment = Comment.objects.create(
            build=self.build, 
            user=self.user2, 
            content="Test comment"
        )
        NotificationService.create_build_comment_notification(self.build, self.user2, comment)
        self.assertEqual(
            Notification.objects.filter(notification_type='build_comment').count(), 
            1
        )
        
        # Test comment vote notification
        NotificationService.create_comment_vote_notification(comment, self.user1, 'upvote')
        self.assertEqual(
            Notification.objects.filter(notification_type='comment_vote').count(), 
            1
        )
        
        # Test mark as read
        notifications = Notification.objects.filter(recipient=self.user1)
        self.assertTrue(all(not n.is_read for n in notifications))
        
        NotificationService.mark_notifications_as_read(self.user1)
        notifications = Notification.objects.filter(recipient=self.user1)
        self.assertTrue(all(n.is_read for n in notifications))

    def test_profile_edit_notification_preferences(self):
        """Test editing notification preferences through profile edit"""
        self.client.login(username='testuser1', password='testpass123')
        
        # Update preferences
        response = self.client.post(reverse('profile-edit'), {
            'first_name': self.user1.first_name,
            'last_name': self.user1.last_name,
            'email': self.user1.email,
            'bio': 'Updated bio',
            'notify_on_build_like': False,
            'notify_on_build_comment': True,
            'notify_on_comment_reply': False,
            'notify_on_comment_vote': True,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit
        
        # Check if preferences were updated
        self.profile1.refresh_from_db()
        self.assertFalse(self.profile1.notify_on_build_like)
        self.assertTrue(self.profile1.notify_on_build_comment)
        self.assertFalse(self.profile1.notify_on_comment_reply)
        self.assertTrue(self.profile1.notify_on_comment_vote)
