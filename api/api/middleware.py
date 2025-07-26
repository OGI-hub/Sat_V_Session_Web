
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings

class SessionTimeoutMiddleware:
    def __call__(self, request):
        print(f"SessionTimeoutMiddleware processing request to {request.path}")
        # Rest of your middleware code
        
class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Check if this is an API request
            if request.path.startswith('/api/'):
                return self.handle_api_session(request)
            else:
                return self.handle_web_session(request)
    
    def handle_api_session(self, request):
        """Handle session timeout for API requests (Token-based)"""
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                # Check if token has expired (custom logic since DRF tokens don't expire by default)
                if hasattr(token, 'created'):
                    token_age = timezone.now() - token.created
                    if token_age.total_seconds() > getattr(settings, 'TOKEN_EXPIRED_AFTER_SECONDS', 3600):
                        token.delete()
                        return JsonResponse({
                            'error': 'Token expired',
                            'expired': True,
                            'redirect': '/auth/login/'
                        }, status=401)
            except Token.DoesNotExist:
                return JsonResponse({
                    'error': 'Invalid token',
                    'expired': True,
                    'redirect': '/auth/login/'
                }, status=401)
    
    def handle_web_session(self, request):
        """Handle session timeout for web requests (Session-based)"""
        last_activity = request.session.get('last_activity')
        
        if last_activity:
            last_activity = timezone.datetime.fromisoformat(last_activity)
            if timezone.now() - last_activity > timedelta(seconds=request.session.get_expiry_age()):
                logout(request)
                request.session.flush()
                return JsonResponse({
                    'error': 'Session expired',
                    'expired': True,
                    'redirect': '/auth/login/'
                }, status=401)
        
        # Update last activity
        request.session['last_activity'] = timezone.now().isoformat()

"""
# api/middleware.py
import ipaddress
import logging
from django.http import JsonResponse
from django.conf import settings

# Set up logging
logger = logging.getLogger('ip_restriction')

class IPRestrictionMiddleware:
    
    Django middleware to restrict access based on client IP
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Convert string networks to IPNetwork objects for efficient checking
        self.allowed_networks = [
            ipaddress.ip_network(network) 
            for network in getattr(settings, 'ALLOWED_IP_NETWORKS', [])
        ]
        # Get exempt paths
        self.exempt_paths = getattr(settings, 'IP_RESTRICTION_EXEMPT_PATHS', [])
        logger.info(f"IP Restriction Middleware initialized with {len(self.allowed_networks)} allowed networks")
        logger.info(f"Exempt paths: {self.exempt_paths}")

    def __call__(self, request):
        # Check if path is exempt from IP restriction
        path = request.path_info
        
        # Check if path is exempt from IP restriction
        for exempt_path in self.exempt_paths:
            if path.startswith(exempt_path):
                logger.debug(f"Path {path} is exempt from IP restriction")
                return self.get_response(request)
                
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        
        # Check if IP is allowed
        try:
            ip_address = ipaddress.ip_address(client_ip)
            is_allowed = any(ip_address in network for network in self.allowed_networks)
            
            logger.info(f"Client IP: {client_ip}, Allowed: {is_allowed}, Path: {path}")
            
            if not is_allowed:
                # Always return a JSON response for API backend
                logger.warning(f"Blocked access from unauthorized IP: {client_ip}")
                
                # Create a restriction ID for display
                import random
                import string
                restriction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                
                return JsonResponse({
                    'error': 'Access denied',
                    'message': 'Your IP address is not authorized to access this application',
                    'ip': client_ip,
                    'restrictionId': restriction_id
                }, status=403)
                
        except ValueError:
            # Invalid IP address
            logger.error(f"Invalid IP address: {client_ip}")
            return JsonResponse({
                'error': 'Access denied',
                'message': 'Invalid IP address',
                'ip': 'invalid'
            }, status=403)
        
        # Continue processing the request
        response = self.get_response(request)
        return response

# Add the AccessDeniedView class directly in the middleware.py file
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class AccessDeniedView(APIView):
    permission_classes = [AllowAny]  # Make sure this is accessible without authentication
    
    def get(self, request):
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        
        # Get IP from query parameters if available
        ip_from_query = request.GET.get('ip')
        if ip_from_query:
            client_ip = ip_from_query
            
        # Log access attempt
        logger.warning(f"Access denied page visited by IP: {client_ip}")
        
        # Create a restriction ID for display
        import random
        import string
        restriction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # Always return JSON response for React SPA
        return Response({
            'error': 'Access denied',
            'message': 'Your IP address is not authorized to access this application',
            'ip': client_ip,
            'restrictionId': restriction_id
        }, status=403)


        
        """