from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SiteConfig
from .forms import SiteConfigForm

@login_required
def branding_settings(request):
    config = SiteConfig.get_config()

    if request.method == "POST":
        form = SiteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            return redirect("branding_settings")
    else:
        form = SiteConfigForm(instance=config)

    return render(request, "branding/settings.html", {"form": form})