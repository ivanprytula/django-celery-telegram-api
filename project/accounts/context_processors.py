from django.conf import settings


def secret_for_invitation(request):
    return {
        'invitation_secret': settings.USER_INVITATION_SECRET
    }
