from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager to create user in the cli."""

    use_in_migrations = True

    def create_user(self, mail, password=None, **extra_fields):
        """Method to create user.

        :param mail: the given mail
        :type mail: str
        :param password: the given password, defaults to None
        :type password: str, optional
        :raises TypeError: no mail given
        :return: the created user
        :rtype: User
        """
        if mail is None:
            raise TypeError("Users must have an email address.")

        user = self.model(mail=self.normalize_email(mail), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, mail, password, **extra_fields):
        """Method to create superuser.

        :param mail: the given mail
        :type mail: str
        :param password: the given password
        :type password: str
        :raises TypeError: No password given, or no mail given
        :return: the super admin user created
        :rtype: User
        """
        if mail is None:
            raise TypeError("Users must have an email address.")

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(mail, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
