from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
