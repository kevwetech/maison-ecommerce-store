import os
from django.core.management.base import BaseCommand
from branding.models import SiteConfig

class Command(BaseCommand):
    help = "Seed SiteConfig from environment variables"

    def handle(self, *args, **kwargs):
        config = SiteConfig.get_config()
        config.site_name = os.environ.get("SITE_NAME", config.site_name)
        config.primary_color = os.environ.get("PRIMARY_COLOR", config.primary_color)
        config.secondary_color = os.environ.get("SECONDARY_COLOR", config.secondary_color)
        config.save()
        self.stdout.write(self.style.SUCCESS("Branding seeded from env vars."))