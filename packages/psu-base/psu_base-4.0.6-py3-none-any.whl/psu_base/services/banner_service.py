from psu_base.services import error_service, utility_service
from django.http import JsonResponse
from psu_base.classes.Log import Log
from psu_base.classes.Finti import Finti

log = Log()
unit_test_session = {'modified': False, 'warned': False}

allowed_name_characters = [
    ' ', '"', '&', "'", '(', ')', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '_', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '|', '~',
    'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë',
    'Ì', 'Í', 'Î', 'Ï', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ù', 'Ú', 'Û', 'Ü',
    'Ý', 'ß',
    'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë',
    'ì', 'í', 'î', 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ù', 'ú', 'û', 'ü', 'ü',
    'ý', 'ÿ',
    'Œ', 'œ', 'Š', 'Ÿ', '˜', '–', '—'
]

special_character_replacements = {
        '\\': '/',
        '[': '(', ']': ')',
        '{': '(', '}': ')',
        '¢': 'c',
        '¥': 'Y',
        'P': 'P',
        'ƒ': 'f',
        'ª': 'a',
        'º': 'o',
        '¬': '-',
        '½': '1/2',
        '¼': '1/4',
        '¦': '|',
        'µ': 'Mu',
        '±': '+-',
        '°': 'o',
        '•': '.',
        '·': '.',
        '²': '2',
        '„': '"',
        '…': '...',
        '†': 't',
        '‘': "'",
        '’': "'",
        '“': '"',
        '”': '"',
        '™': 'TM',
        'š': 's',
        '©': '(c)',
        '®': '(R)',
        '¯': '-',
        '³': '3',
        '´': "'",
        '¸': ',',
        '¹': '1',
        '¾': '3/4',
        'Ð': 'D',
        '×': 'x',
        'Ø': '0',
        '÷': '/',
        'ø': 'o',
    }


def clean_name(name):
    """Remove non-allowed characters, doing conversions when possible"""

    name_changed = False
    if name:
        cleaned = ''
        for cc in str(name):
            if cc in allowed_name_characters:
                cleaned += cc
            elif cc in special_character_replacements:
                cleaned += special_character_replacements[cc]
                name_changed = True
            else:
                # Character is removed
                name_changed = True
        name = cleaned

    return name, name_changed


def clean_special_characters(content):
    """
    Remove non-allowed characters, doing conversions when possible
    - Less strict than clean_name()
    """
    content_changed = False
    if content:
        cleaned = ''
        for cc in str(content):
            # Allow all basic ascii characters
            if 32 <= ord(cc) <= 126:
                cleaned += cc
            # Allow any special characters allowed in names
            elif cc in allowed_name_characters:
                cleaned += cc
            # Attempt to replace other special characters
            elif cc in special_character_replacements:
                cleaned += special_character_replacements[cc]
                content_changed = True
            # Remove any other characters
            else:
                # Character is removed
                content_changed = True
        content = cleaned

    return content, content_changed


def finti_get_json_response(path, parameters=None, include_metadata=False):
    """
    Make a GET request and return the result as a JsonResponse with appropriate HTTP status code
    """
    finti = Finti()
    response = JsonResponse(Finti().get(path=path, parameters=parameters, include_metadata=include_metadata))
    response.status_code = finti.http_status_code
    return response


def finti_post_json_response(path, payload=None, headers=None, include_metadata=False, json_payload=None):
    """
    Make a POST request and return the result as a JsonResponse with appropriate HTTP status code
    """
    finti = Finti()
    response = JsonResponse(Finti().post(
        path, payload=payload, headers=headers, include_metadata=include_metadata, json_payload=json_payload
    ))
    response.status_code = finti.http_status_code
    return response


def finti_get_menu_options_response(menu_type):
    """
    Get menu options from Banner validation tables as a JsonResponse with appropriate HTTP status code
    """
    finti = Finti()
    response = JsonResponse(finti_get_menu_options(menu_type, finti))
    response.status_code = finti.http_status_code
    return response


def finti_get_menu_options(menu_type, finti_instance=None):
    """
    Get menu options from Banner validation tables.
    Examples of menu_type include state, nation, race, ethnicity, ...
    The complete list of available menu_types is only found in Banner: api/dbprocs/zwd_form_options
    """
    log.trace([menu_type])

    # Get a new Finti instance if not provided
    # (Instance might be provided for error/status tracking from the calling function)
    if finti_instance is None:
        finti_instance = Finti()

    # Get the menu options
    options = finti_instance.get(f'wdt/v1/menu_options/{menu_type}')

    # If options were not found, log the error message and return an empty dict
    if not finti_instance.successful:
        log.error(options)
        return {}

    # Otherwise, return the options as a dict
    else:
        return utility_service.options_list_to_dict(options)
