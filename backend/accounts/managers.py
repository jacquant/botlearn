from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, mail, password=None, **extra_fields):

        if mail is None:
            raise TypeError("Users must have an email address.")

        user = self.model(mail=self.normalize_email(mail), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, mail, password, **extra_fields):

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(mail, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
