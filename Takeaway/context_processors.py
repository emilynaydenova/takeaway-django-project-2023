# https://dev.to/gilbishkosma/custom-context-processors-in-django-3c93
def common_variables(request):

    context = {
        'logo_name': 'TastyFood',
        'logged_in_user': request.user.is_authenticated,
    }
    return context

# add in settings -> Templates -> Options
# 'takeaway.context_processors.common_variables',
