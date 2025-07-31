"""
Management command to check and set up Cloudinary configuration
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Check and guide setup of Cloudinary configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌥️  Cloudinary Configuration Check'))
        self.stdout.write('=' * 50)
        
        # Check if Cloudinary environment variables are set
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
        api_key = os.environ.get('CLOUDINARY_API_KEY', '')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')
        
        if cloud_name and api_key and api_secret:
            self.stdout.write(self.style.SUCCESS('✅ Cloudinary credentials are configured!'))
            self.stdout.write(f'Cloud Name: {cloud_name}')
            self.stdout.write(f'API Key: {api_key[:8]}...')
            self.stdout.write('API Secret: [HIDDEN]')
        else:
            self.stdout.write(self.style.WARNING('⚠️  Cloudinary credentials not found!'))
            self.stdout.write('')
            self.stdout.write('To set up Cloudinary:')
            self.stdout.write('1. Sign up at https://cloudinary.com/')
            self.stdout.write('2. Get your credentials from the dashboard')
            self.stdout.write('3. Set environment variables:')
            self.stdout.write('')
            self.stdout.write('   Windows (Command Prompt):')
            self.stdout.write('   set CLOUDINARY_CLOUD_NAME=your_cloud_name')
            self.stdout.write('   set CLOUDINARY_API_KEY=your_api_key')
            self.stdout.write('   set CLOUDINARY_API_SECRET=your_api_secret')
            self.stdout.write('')
            self.stdout.write('   Windows (PowerShell):')
            self.stdout.write('   $env:CLOUDINARY_CLOUD_NAME="your_cloud_name"')
            self.stdout.write('   $env:CLOUDINARY_API_KEY="your_api_key"')
            self.stdout.write('   $env:CLOUDINARY_API_SECRET="your_api_secret"')
            self.stdout.write('')
            self.stdout.write('   Or create a .env file in your project root:')
            self.stdout.write('   CLOUDINARY_CLOUD_NAME=your_cloud_name')
            self.stdout.write('   CLOUDINARY_API_KEY=your_api_key')
            self.stdout.write('   CLOUDINARY_API_SECRET=your_api_secret')
            self.stdout.write('')
            
        # Test Cloudinary connection
        if cloud_name and api_key and api_secret:
            try:
                import cloudinary.api
                result = cloudinary.api.ping()
                if result.get('status') == 'ok':
                    self.stdout.write(self.style.SUCCESS('✅ Cloudinary connection test successful!'))
                else:
                    self.stdout.write(self.style.ERROR('❌ Cloudinary connection test failed'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Cloudinary connection error: {str(e)}'))
        
        self.stdout.write('')
        self.stdout.write('Image transformations configured:')
        self.stdout.write('• Profile pictures: Auto-optimized, face detection, rounded corners')
        self.stdout.write('• Build images: Auto-optimized, multiple sizes available')
        self.stdout.write('• Automatic format selection (WebP, AVIF when supported)')
        self.stdout.write('• Quality optimization based on content type')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🚀 Ready to use Cloudinary for image management!'))
