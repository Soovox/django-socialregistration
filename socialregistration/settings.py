from django.conf import settings

SESSION_KEY = getattr(settings, 'SOCIALREGISTRATION_SESSION_KEY', 'socialreg:')
AFTER_SIGNUP = getattr(settings, 'SOCIALREGISTRATION_AFTER_SIGNUP', '/')