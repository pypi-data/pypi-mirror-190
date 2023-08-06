from django.shortcuts import redirect
from psu_base.services import utility_service
from psu_base.classes.Log import Log
from django.http import HttpResponseForbidden
from psu_base.services import utility_service
from psu_base.services import auth_service
from psu_base.classes.IdentityCAS import IdentityCAS
from psu_base.classes.Finti import Finti
from django.urls import reverse

from django.conf import settings
from django.contrib.auth.decorators import login_required
import re

log = Log()


class PsuBaseMiddleware:
    def __init__(self, get_response):
        log.trace(["IS THIS RUNNING??? -- INIT"])
        self.get_response = get_response
        # One-time configuration and initialization.

        # Public views are defined in settings.py for each app: <APP_CODE>_PUBLIC_URLS
        #
        # As new public views are added to psu_base, the PSU_PUBLIC_URLS setting would need to be updated for
        # every existing app.  To avoid that, public psu_base views will now be listed here instead:
        psu_public_urls = [
            '.*/accounts/login', '.*/psu/messages', '.*/psu/test',
            '.*/psu/validate/date', '.*/psu/format/phone_number',
            '.*/psu/menu_options/*',
        ]

        # Authentication will be required on all pages, unless defined as public in settings
        self.public_views = []
        for ss in dir(settings):
            if ss.endswith("PUBLIC_URLS") and ss != 'PSU_PUBLIC_URLS':
                urls = tuple(re.compile(url) for url in getattr(settings, ss))
                if urls:
                    self.public_views += list(urls)
        # Add in the PSU_BASE public URLs
        urls = tuple(re.compile(url) for url in psu_public_urls)
        if urls:
            self.public_views += list(urls)

        log.debug(f"PUBLIC URLS: {str(self.public_views)}")

    def process_view(self, request, view_func, view_args, view_kwargs):
        # By default, all pages require authentication
        # This can be disabled by setting REQUIRE_LOGIN to False in app_settings.py
        # When disabled, authentication will still be required for most psu plugin-provided views

        # No checking required when user is already authenticated
        if request.user.is_authenticated:
            return None

        # If requirement disabled, only need to check /psu/ urls
        elif '/psu/' not in request.path and not settings.REQUIRE_LOGIN:
            return None

        # Now, either all pages require auth, or this is a /psu/ path which may require auth
        else:
            # Has this page been defined as public?
            is_public = False
            for url in self.public_views:
                if url.match(request.path):
                    is_public = True

            # If public, no auth required
            if is_public:
                return None
            # Otherwise, require auth
            else:
                log.info(f"Authentication required for path: {request.path}")
                return login_required(view_func, login_url='cas:login')(request, *view_args, **view_kwargs)

    def __call__(self, request):
        # Is this an AWS health check or flash messages?
        flash_messages = request.path == reverse('psu:messages')
        silence_logs = utility_service.is_health_check() or flash_messages

        # In non-prod, make the start of a new request more visible in the log (console)
        if not silence_logs:
            if utility_service.is_non_production():
                w = 80
                log.debug(f"\n{'='.ljust(w, '=')}\n{'New Request'.center(w)}\n{'='.ljust(w, '=')}")
            log.trace([request.path], 'psu_base request')
        elif flash_messages:
            log.debug("Processing 'Flash Messages'...")

        # Remove flash variables from two requests ago. Shift flash variables from last request.
        # This happens for every request EXCEPT posting flash messages to the screen
        if not flash_messages:
            utility_service.cycle_flash_scope()
            app_code = utility_service.get_app_code()
            sub_app_info = utility_service.get_sub_app_info()
            if sub_app_info.get('last_app') and not silence_logs:
                log.debug(f"Sub-App Info: {sub_app_info}")

        # Before the view (and later middleware) are called.
        auth_service.set_sso_user(request)

        if not silence_logs:
            auth_str = ""
            for u in ['sso_user', 'impersonated_user', 'proxied_user']:
                try:
                    auth_str += f"<{u}: {request.session.get('psu_base_auth_object').get(u).get('username')}>, "
                except:
                    auth_str += f"<{u}: None>, "
            log.info(auth_str)

        # Render the response
        response = self.get_response(request)

        # After the view has completed
        utility_service.clear_page_scope()

        if not silence_logs:
            log.end(None, 'psu_base request')

        return response
