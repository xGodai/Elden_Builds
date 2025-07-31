from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Notification
from .notifications import NotificationService


@login_required
def notification_list(request):
    """Display user's notifications"""
    notifications = Notification.objects.filter(recipient=request.user)
    unread_count = NotificationService.get_unread_count(request.user)
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'users/notifications.html', context)


@login_required
@require_http_methods(["POST"])
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.mark_as_read()
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True})
        
        return redirect('notification-list')
    except Exception as e:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        
        messages.error(request, 'Error marking notification as read.')
        return redirect('notification-list')


@login_required
@require_http_methods(["POST"])
def mark_notifications_read(request):
    """Mark multiple notifications as read"""
    try:
        notification_ids = request.POST.getlist('notification_ids')
        if notification_ids:
            NotificationService.mark_notifications_as_read(request.user, notification_ids)
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_http_methods(["POST"])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    try:
        NotificationService.mark_notifications_as_read(request.user)
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True})
        
        messages.success(request, 'All notifications marked as read.')
        return redirect('notification-list')
    except Exception as e:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        
        messages.error(request, 'Error marking notifications as read.')
        return redirect('notification-list')


@login_required
@require_http_methods(["POST"])
def delete_notification(request, notification_id):
    """Delete a specific notification"""
    try:
        success = NotificationService.delete_notification(notification_id, request.user)
        
        if success:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': True})
            
            messages.success(request, 'Notification deleted.')
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'error': 'Notification not found'})
            
            messages.error(request, 'Notification not found.')
        
        return redirect('notification-list')
    except Exception as e:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': False, 'error': str(e)})
        
        messages.error(request, 'Error deleting notification.')
        return redirect('notification-list')


@login_required
def get_unread_count(request):
    """Get unread notification count for AJAX requests"""
    count = NotificationService.get_unread_count(request.user)
    return JsonResponse({'count': count})
