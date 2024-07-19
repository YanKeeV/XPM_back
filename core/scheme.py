from drf_spectacular.extensions import OpenApiAuthenticationExtension
from core.backends import JWTAuthentication

class JWTScheme(OpenApiAuthenticationExtension):
    target_class = 'core.backends.JWTAuthentication'
    name = 'JWTAuthentication'
    match_subclasses = True
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }