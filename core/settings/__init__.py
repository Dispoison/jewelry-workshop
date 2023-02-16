from core.settings.base import *

if env("ENVIRONMENT") == "production":
    from core.settings.production import *
elif env("ENVIRONMENT") == "development":
    from core.settings.development import *
else:
    raise ValueError("Environment variable 'ENVIRONMENT' must be equal 'development' or 'production'")
