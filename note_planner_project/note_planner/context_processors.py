from .models import UserProfilePhoto


def get_user_profile_photo(request):
    user = request.user

    if user.is_authenticated:
        photo = UserProfilePhoto.objects.filter(user=user, main_photo=True)
        if photo.exists():
            photo = photo.latest('main_photo').photo


    else:
        photo = None

    return {'user_profile_photo': photo}

