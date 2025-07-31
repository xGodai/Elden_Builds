"""
Cloudinary utilities for image transformations and URL generation
"""
from cloudinary import CloudinaryImage
from cloudinary.utils import cloudinary_url


def get_optimized_image_url(public_id, **transformations):
    """
    Generate an optimized image URL with transformations
    
    Args:
        public_id (str): The Cloudinary public ID of the image
        **transformations: Cloudinary transformation parameters
    
    Returns:
        str: Optimized image URL
    """
    if not public_id:
        return None
    
    default_transformations = {
        'quality': 'auto',
        'fetch_format': 'auto',
    }
    
    # Merge default transformations with custom ones
    all_transformations = {**default_transformations, **transformations}
    
    url, options = cloudinary_url(public_id, **all_transformations)
    return url


def get_profile_picture_url(cloudinary_field, size=300):
    """
    Get optimized profile picture URL
    
    Args:
        cloudinary_field: CloudinaryField instance
        size (int): Desired size for square crop
    
    Returns:
        str: Optimized profile picture URL
    """
    if not cloudinary_field:
        return None
    
    return get_optimized_image_url(
        cloudinary_field.public_id,
        width=size,
        height=size,
        crop='fill',
        gravity='face',
        radius='max' if size <= 150 else 20,  # Make small images circular
        quality='auto:good'
    )


def get_build_image_url(cloudinary_field, width=800, height=600):
    """
    Get optimized build image URL
    
    Args:
        cloudinary_field: CloudinaryField instance  
        width (int): Desired width
        height (int): Desired height
    
    Returns:
        str: Optimized build image URL
    """
    if not cloudinary_field:
        return None
    
    return get_optimized_image_url(
        cloudinary_field.public_id,
        width=width,
        height=height,
        crop='fill',
        quality='auto:good'
    )


def get_thumbnail_url(cloudinary_field, width=300, height=200):
    """
    Get optimized thumbnail URL
    
    Args:
        cloudinary_field: CloudinaryField instance
        width (int): Desired width
        height (int): Desired height
    
    Returns:
        str: Optimized thumbnail URL
    """
    if not cloudinary_field:
        return None
    
    return get_optimized_image_url(
        cloudinary_field.public_id,
        width=width,
        height=height,
        crop='fill',
        quality='auto:eco'  # Lower quality for thumbnails
    )


# Preset transformation configurations
PROFILE_SIZES = {
    'small': {'width': 50, 'height': 50},
    'medium': {'width': 150, 'height': 150},
    'large': {'width': 300, 'height': 300},
}

BUILD_SIZES = {
    'thumbnail': {'width': 300, 'height': 200},
    'medium': {'width': 600, 'height': 400},
    'large': {'width': 1200, 'height': 800},
}
