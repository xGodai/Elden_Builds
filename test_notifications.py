#!/usr/bin/env python
"""
Simple test script to verify notification system is working
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eldenring_project.settings')
django.setup()

from django.contrib.auth.models import User
from builds.models import Build, Comment, CommentVote
from users.models import Notification, UserProfile
from users.notifications import NotificationService

def test_notification_system():
    print("🧪 Testing notification system...")
    
    # Create test users
    user1 = User.objects.get_or_create(username='testuser1', defaults={
        'email': 'test1@example.com',
        'first_name': 'Test',
        'last_name': 'User1'
    })[0]
    
    user2 = User.objects.get_or_create(username='testuser2', defaults={
        'email': 'test2@example.com',
        'first_name': 'Test',
        'last_name': 'User2'
    })[0]
    
    # Ensure user profiles exist with notification preferences enabled
    profile1, created = UserProfile.objects.get_or_create(user=user1, defaults={
        'notify_on_build_like': True,
        'notify_on_build_comment': True,
        'notify_on_comment_reply': True,
        'notify_on_comment_vote': True
    })
    profile2, created = UserProfile.objects.get_or_create(user=user2, defaults={
        'notify_on_build_like': True,
        'notify_on_build_comment': True,
        'notify_on_comment_reply': True,
        'notify_on_comment_vote': True
    })
    
    # Make sure preferences are enabled for existing profiles
    profile1.notify_on_build_like = True
    profile1.notify_on_build_comment = True
    profile1.notify_on_comment_reply = True
    profile1.notify_on_comment_vote = True
    profile1.save()
    
    profile2.notify_on_build_like = True
    profile2.notify_on_build_comment = True
    profile2.notify_on_comment_reply = True
    profile2.notify_on_comment_vote = True
    profile2.save()
    
    print(f"✅ Created/found users with notification preferences: {user1.username}, {user2.username}")
    
    # Clear existing notifications for clean test
    Notification.objects.filter(recipient__in=[user1, user2]).delete()
    
    # Create a test build
    build = Build.objects.create(
        user=user1,
        title="Test Notification Build",
        description="This is a test build for notifications",
        weapons="Test Weapon",
        armor="Test Armor",
        talismans="Test Talisman",
        spells="Test Spell",
        category="PVE"
    )
    print(f"✅ Created test build: {build.title}")
    
    # Test 1: Build like notification
    print("\n🔔 Testing build like notification...")
    NotificationService.create_build_like_notification(build, user2)
    
    notifications = Notification.objects.filter(recipient=user1, notification_type='build_like')
    if notifications.exists():
        print(f"✅ Build like notification created: {notifications.first().message}")
    else:
        print("❌ Build like notification failed")
    
    # Test 2: Build comment notification
    print("\n🔔 Testing build comment notification...")
    comment = Comment.objects.create(
        build=build,
        user=user2,
        content="This is a test comment for notifications"
    )
    
    NotificationService.create_build_comment_notification(build, user2, comment)
    
    notifications = Notification.objects.filter(recipient=user1, notification_type='build_comment')
    if notifications.exists():
        print(f"✅ Build comment notification created: {notifications.first().message}")
    else:
        print("❌ Build comment notification failed")
    
    # Test 3: Comment vote notification
    print("\n🔔 Testing comment vote notification...")
    print(f"User2 profile notify_on_comment_vote: {profile2.notify_on_comment_vote}")
    NotificationService.create_comment_vote_notification(comment, user1, 'upvote')
    
    notifications = Notification.objects.filter(recipient=user2, notification_type='comment_vote')
    if notifications.exists():
        print(f"✅ Comment vote notification created: {notifications.first().message}")
    else:
        print("❌ Comment vote notification failed")
    
    # Test 4: Check notification preferences
    print("\n⚙️ Testing notification preferences...")
    profile1.notify_on_build_like = False
    profile1.save()
    
    # This should not create a notification
    NotificationService.create_build_like_notification(build, user2)
    new_notifications = Notification.objects.filter(
        recipient=user1, 
        notification_type='build_like'
    ).count()
    
    if new_notifications == 1:  # Should still be 1 (from earlier test)
        print("✅ Notification preferences working correctly")
    else:
        print("❌ Notification preferences not working")
    
    print(f"\n📊 Total notifications created: {Notification.objects.count()}")
    
    # Show all notifications
    print("\n📋 All notifications:")
    for notification in Notification.objects.all():
        print(f"  • {notification.recipient.username}: {notification.message} ({notification.notification_type})")
    
    print("\n🎉 Notification system test completed!")

if __name__ == '__main__':
    test_notification_system()
