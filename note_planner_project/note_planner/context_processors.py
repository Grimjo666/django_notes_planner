from .models import UserProfileInfo


def get_user_profile_photo(request):
    user = request.user

    if user.is_authenticated:
        photo = UserProfileInfo.objects.filter(user=user)
        if photo.exists():
            photo = photo.latest('load_at').photo

    else:
        photo = None

    return {'user_profile_photo': photo}

