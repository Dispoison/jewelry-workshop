from core.settings.base import *

if env("PRODUCTION") is True:
   from core.settings.production import *
else:
   from core.settings.development import *
