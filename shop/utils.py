from django.contrib.auth import get_user_model

def authenticate_user(email=None, password=None):
    UserModel = get_user_model()
    if email is None or password is None:
        return None
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None
    if user.check_password(password):
        return user
    return None