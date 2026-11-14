from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .auth0 import oauth


def auth0_login(request):
    next_url = request.GET.get("next", reverse("admin:index"))

    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure()
    ):
        next_url = reverse("admin:index")

    request.session["auth0_next"] = next_url

    redirect_uri = settings.AUTH0_CALLBACK_URL

    return oauth.auth0.authorize_redirect(request, redirect_uri)


def auth0_callback(request):
    token = oauth.auth0.authorize_access_token(request)

    userinfo = token.get("userinfo")

    if not userinfo:
        return HttpResponseForbidden("No se pudo verificar tu identidad.")

    email = userinfo.get("email")

    if not email or not userinfo.get("email_verified"):
        return HttpResponseForbidden("Necesitas un correo verificado.")

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return HttpResponseForbidden("No tienes una cuenta Django registrada.")

    if not user.is_active or not user.is_staff:
        return HttpResponseForbidden("No tienes permisos para acceder al Admin.")

    login(
        request,
        user,
        backend="django.contrib.auth.backends.ModelBackend"
    )

    next_url = request.session.pop(
        "auth0_next",
        reverse("admin:index")
    )

    return redirect(next_url)


def auth0_logout(request):
    logout(request)
    return redirect("auth0_login")