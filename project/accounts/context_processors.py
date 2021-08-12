from django.conf import settings


def secret_for_invitation(request):
    if request.path == '/':
        return {
            'invitation_secret': settings.USER_INVITATION_SECRET
        }
    else:
        return {}
