from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email=None, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError("No login")

        user = self.model(
            email=email,
            name=name if name else 'User',
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, login, password, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError(_('Superuser must have is_staff=True.'))
    #     return self.create_user(login=login, password=password, **extra_fields)
        