import os
from .models import SiteConfig

def site_branding(request):
    """
    Two-layer fallback:
    1. Database (SiteConfig row)
    2. Environment variables
    3. Hardcoded defaults
    """
    env = {
        "site_name": os.environ.get("SITE_NAME", "My Store"),
        "primary_color": os.environ.get("PRIMARY_COLOR", "#4F46E5"),
        "secondary_color": os.environ.get("SECONDARY_COLOR", "#10B981"),
        "logo_url": os.environ.get("LOGO_URL", ""),
    }

    try:
        db = SiteConfig.get_config()
        branding = {
            "site_name": db.site_name or env["site_name"],
            "primary_color": db.primary_color or env["primary_color"],
            "secondary_color": db.secondary_color or env["secondary_color"],
            "logo_url": db.logo.url if db.logo else env["logo_url"],
        }
    except Exception:
        # DB unavailable (migrations not run yet, etc.)
        branding = env

    return {"branding": branding}