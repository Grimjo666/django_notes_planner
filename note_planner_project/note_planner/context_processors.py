from .models import UserProfilePhoto
from django.contrib.auth.models import User


def get_user_profile_photo(request):
    user = request.user
    user_name = None
    photo = None

    if user.is_authenticated:
        photo = UserProfilePhoto.objects.filter(user=user, main_photo=True)
        if photo.exists():
            photo = photo.latest('main_photo').photo

        user_info = User.objects.get(id=user.id)
        user_first_name = user_info.first_name
        user_last_name = user_info.last_name

        if len(user_first_name + user_last_name) != 0:
            user_name = f'{user_first_name} {user_last_name}'

    return {
        'user_profile_photo': photo,
        'user_name': user_name,
            }

