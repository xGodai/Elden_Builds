from users.models import Notification


def notification_context(request):
    """
    Context processor to add notification count to all templates
    """
    context = {}

    if request.user.is_authenticated:
        context['unread_count'] = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
    else:
        context['unread_count'] = 0

    return context
