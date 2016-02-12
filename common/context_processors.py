from django.contrib.auth.forms import AuthenticationForm

def common_forms(request):
    return {
        'login_form': AuthenticationForm()
    }
