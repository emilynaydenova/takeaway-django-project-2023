# https://dev.to/gilbishkosma/custom-context-processors-in-django-3c93
from decouple import config


def common_variables(request):
    """
          The context processor must return a dictionary.
        """
    context = {
        'logo_name': config('LOGO_NAME'),
        'logged_in_user': request.user.is_authenticated,
    }
    return context

# add in settings -> Templates -> Options -> path
# 'common.context_processors.common_variables',
