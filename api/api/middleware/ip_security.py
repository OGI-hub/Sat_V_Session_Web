

# Create a new file: api/middleware/ip_security.py

import ipaddress
from django.conf import settings
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)



class IPSecurityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # Load allowed IP ranges from settings
        self.allowed_ips = getattr(settings, 'ALLOWED_IP_RANGES', [])
        self.allowed_networks = []
        
        # Convert string IP ranges to network objects
        for ip_range in self.allowed_ips:
            try:
                # Handle both individual IPs and CIDR notations
                network = ipaddress.ip_network(ip_range, strict=False)
                self.allowed_networks.append(network)
            except ValueError as e:
                logger.error(f"Invalid IP range in settings: {ip_range}. Error: {str(e)}")
        
        # Debug output
        logger.info(f"IP Security Middleware initialized with {len(self.allowed_networks)} networks")
        for network in self.allowed_networks:
            logger.info(f"Allowing access from network: {network}")
    
    def __call__(self, request):
       
       # Skip IP check for ALLOWED_IP_BYPASS_PATHS
       path = request.path
       bypass_paths = getattr(settings, 'ALLOWED_IP_BYPASS_PATHS', [])
       if any(path.startswith(bypass_path) for bypass_path in bypass_paths):
        logger.info(f"BYPASS: Path {path} is in bypass list")
        return self.get_response(request)
    
       # Get client IP
       x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
       if x_forwarded_for:
        # If behind a proxy, get the real IP
        ip = x_forwarded_for.split(',')[0].strip()
       else:
        ip = request.META.get('REMOTE_ADDR')
    
       # Check if IP is allowed
       client_ip = ipaddress.ip_address(ip)
       logger.info(f"CHECKING: IP {ip} against {len(self.allowed_networks)} networks")
    
       # Enhanced logging for each network check
       for network in self.allowed_networks:
        if client_ip in network:
            logger.info(f"ALLOWED: IP {ip} in network {network}")
            return self.get_response(request)
        logger.info(f"NOT MATCHED: IP {ip} not in network {network}")
    
       # Log the blocked attempt
       logger.warning(f"BLOCKED: Access denied for IP: {ip}, path: {request.path}")
    
       # IP is not allowed, return 403 Forbidden
       return HttpResponseForbidden(
        "<h1>Access Denied</h1><p>Your IP address is not authorized to access this resource.</p>"
    ) 