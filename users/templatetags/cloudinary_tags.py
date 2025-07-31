from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def cloudinary_image(image_field, size='medium', css_class='', alt_text=''):
    """
    Template tag for rendering optimized Cloudinary images
    
    Usage:
    {% cloudinary_image build.image 'large' 'img-fluid' 'Build image' %}
    {% cloudinary_image user.profile.profile_picture 'small' 'rounded-circle' 'Profile picture' %}
    """
    if not image_field:
        return ''
    
    # Determine if this is a profile picture or build image
    if hasattr(image_field, 'folder') and 'profile' in str(image_field.folder):
        # This is a profile picture
        if hasattr(image_field, '_meta') and hasattr(image_field._meta, 'model'):
            # Get URL from the model method
            url = image_field._meta.model.get_profile_picture_url(size)
        else:
            from utils.cloudinary_utils import get_profile_picture_url, PROFILE_SIZES
            size_config = PROFILE_SIZES.get(size, PROFILE_SIZES['medium'])
            url = get_profile_picture_url(image_field, size_config['width'])
    else:
        # This is a build image
        from utils.cloudinary_utils import get_build_image_url, get_thumbnail_url, BUILD_SIZES
        if size == 'thumbnail':
            url = get_thumbnail_url(image_field)
        else:
            size_config = BUILD_SIZES.get(size, BUILD_SIZES['medium'])
            url = get_build_image_url(image_field, size_config['width'], size_config['height'])
    
    if not url:
        return ''
    
    # Build the img tag
    css_class = f'class="{css_class}"' if css_class else ''
    alt_text = f'alt="{alt_text}"' if alt_text else 'alt=""'
    
    img_tag = f'<img src="{url}" {css_class} {alt_text} loading="lazy">'
    return mark_safe(img_tag)


@register.simple_tag
def cloudinary_url(image_field, size='medium'):
    """
    Template tag for getting optimized Cloudinary image URLs
    
    Usage:
    <img src="{% cloudinary_url build.image 'large' %}" alt="Build image">
    """
    if not image_field:
        return ''
    
    # Determine if this is a profile picture or build image
    if hasattr(image_field, 'folder') and 'profile' in str(image_field.folder):
        from utils.cloudinary_utils import get_profile_picture_url, PROFILE_SIZES
        size_config = PROFILE_SIZES.get(size, PROFILE_SIZES['medium'])
        return get_profile_picture_url(image_field, size_config['width'])
    else:
        from utils.cloudinary_utils import get_build_image_url, get_thumbnail_url, BUILD_SIZES
        if size == 'thumbnail':
            return get_thumbnail_url(image_field)
        else:
            size_config = BUILD_SIZES.get(size, BUILD_SIZES['medium'])
            return get_build_image_url(image_field, size_config['width'], size_config['height'])


@register.filter
def profile_picture(user, size='medium'):
    """
    Template filter for getting user profile pictures
    
    Usage:
    {{ user|profile_picture:'small' }}
    """
    if hasattr(user, 'profile') and user.profile:
        return user.profile.get_profile_picture_url(size)
    return f"https://ui-avatars.com/api/?name={user.username}&background=6c757d&color=ffffff&size=150"
