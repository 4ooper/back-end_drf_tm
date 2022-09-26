from .models import User
from django.db.models import Q

# class AuthBackend(object):
#     supports_object_permissions = True
    
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

#     def authenficate(self, request, email, password):
#         try:
#             print('try')
#             user = User.objects.get(Q(email=email))
#         except User.DoesNotExist:
#             return None

#         return user if user.check_password(password) else None