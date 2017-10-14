from .models import UserLevel


def exp(request):
    levels = UserLevel.objects.all()
    return {'levels': levels}
