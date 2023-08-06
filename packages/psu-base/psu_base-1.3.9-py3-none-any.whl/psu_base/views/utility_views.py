# utility_views.py
#
#   These are views that are used for common tasks
#

from django.http import HttpResponse, HttpResponseBadRequest
from psu_base.classes.Log import Log
from psu_base.classes.ConvenientDate import ConvenientDate
from psu_base.classes.DynamicRole import DynamicRole

log = Log()
allowable_role_list = DynamicRole().super_user()


def validate_date_format(request):
    """
    Given a date input, validate the date format and return in standard format, or Forbidden if invalid

    Params:
        date_string:    The date entered by the user
        response_type:  Optional - { date, datetime } (defaults to 'date')
    """
    date_string = request.GET.get('date_string')
    response_type = request.GET.get('response_type', 'date')
    log.trace(date_string)

    if not date_string:
        return HttpResponseBadRequest()

    date_cd = ConvenientDate(date_string)

    if date_cd.conversion_error:
        log.warning(date_cd.conversion_error)
        return HttpResponseBadRequest()
    elif not date_cd.datetime_instance:
        log.warning("Unable to validate date format")
        return HttpResponseBadRequest()

    if 'time' in response_type.lower():
        return HttpResponse(date_cd.timestamp())
    else:
        return HttpResponse(date_cd.date_field())
