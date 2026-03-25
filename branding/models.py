from django.db import models

class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default="My Store")
    logo = models.ImageField(upload_to="branding/", null=True, blank=True)
    primary_color = models.CharField(max_length=7, default="#4F46E5")   # hex
    secondary_color = models.CharField(max_length=7, default="#10B981")

    class Meta:
        verbose_name = "Site Configuration"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_config(cls):
        """Always returns one config row, creating it if missing."""
        config, _ = cls.objects.get_or_create(pk=1)
        return config