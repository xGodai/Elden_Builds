from .models import Notification


class NotificationService:
    """Service class for creating and managing notifications"""

    @staticmethod
    def create_build_like_notification(build, liker):
        """Create notification when someone likes a build"""
        if build.user == liker:
            return  # Don't notify if user likes their own build

        if not build.user.profile.notify_on_build_like:
            return  # User has disabled this notification type

        # Check if notification already exists to avoid duplicates
        existing = Notification.objects.filter(
            recipient=build.user,
            sender=liker,
            notification_type='build_like',
            build=build
        ).first()

        if existing:
            return  # Notification already exists

        message = f"{
            liker.profile.get_display_name()} liked your build '{
            build.title}'"

        Notification.objects.create(
            recipient=build.user,
            sender=liker,
            notification_type='build_like',
            build=build,
            message=message
        )

    @staticmethod
    def create_build_comment_notification(build, commenter, comment):
        """Create notification when someone comments on a build"""
        if build.user == commenter:
            return  # Don't notify if user comments on their own build

        if not build.user.profile.notify_on_build_comment:
            return  # User has disabled this notification type

        message = f"{
            commenter.profile.get_display_name()} commented on your build '{
            build.title}'"

        Notification.objects.create(
            recipient=build.user,
            sender=commenter,
            notification_type='build_comment',
            build=build,
            comment=comment,
            message=message
        )

    @staticmethod
    def create_comment_vote_notification(comment, voter, vote_type):
        """Create notification when someone votes on a comment"""
        if comment.user == voter:
            return  # Don't notify if user votes on their own comment

        if not comment.user.profile.notify_on_comment_vote:
            return  # User has disabled this notification type

        # Only notify for upvotes to reduce spam
        if vote_type != 'upvote':
            return

        # Check if notification already exists for this vote type
        existing = Notification.objects.filter(
            recipient=comment.user,
            sender=voter,
            notification_type='comment_vote',
            comment=comment
        ).first()

        if existing:
            return  # Notification already exists

        message = f"{
            voter.profile.get_display_name()} upvoted your comment on '{
            comment.build.title}'"

        Notification.objects.create(
            recipient=comment.user,
            sender=voter,
            notification_type='comment_vote',
            comment=comment,
            build=comment.build,
            message=message
        )

    @staticmethod
    def mark_notifications_as_read(user, notification_ids=None):
        """Mark notifications as read"""
        queryset = Notification.objects.filter(recipient=user)

        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)

        queryset.update(is_read=True)

    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user"""
        return Notification.objects.filter(
            recipient=user, is_read=False).count()

    @staticmethod
    def get_recent_notifications(user, limit=10):
        """Get recent notifications for a user"""
        return Notification.objects.filter(recipient=user)[:limit]

    @staticmethod
    def delete_notification(notification_id, user):
        """Delete a specific notification if it belongs to the user"""
        try:
            notification = Notification.objects.get(
                id=notification_id, recipient=user)
            notification.delete()
            return True
        except Notification.DoesNotExist:
            return False
