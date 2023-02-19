from core.settings.base import *

environment = env("ENVIRONMENT")

if environment == PRODUCTION_ENVIRONMENT:
    from core.settings.production import *
elif environment == DEVELOPMENT_ENVIRONMENT:
    from core.settings.development import *
else:
    raise ValueError(f"Environment variable 'ENVIRONMENT' must be equal "
                     f"'{DEVELOPMENT_ENVIRONMENT}' or '{PRODUCTION_ENVIRONMENT}'")
