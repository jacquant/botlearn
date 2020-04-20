from rest_framework import serializers

from accounts.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """Custom Serialiser used with the User Model."""

    class Meta(object):
        """Meta class of the UserSerializer."""

        model = User
        fields = (
            "mail",
            "last_name",
            "first_name",
            "student",
            "student_card",
            "eid",
            "is_staff",
        )

    def create(self, validated_data):
        """Create method used to create a new user.

        :param validated_data: The data that respect the model properties.
        :type validated_data: dict
        :return: The saved user object
        :rtype: User
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Update method used to change a specific user.

        :param instance: the user instance to change
        :type instance: User object
        :param validated_data: The data that will be used to modify the user.
        :type validated_data: dict
        :return: The updated user object
        :rtype: User
        """
        for attr, validated_item in validated_data.items():
            if attr == "password":
                instance.set_password(validated_item)
            else:
                setattr(instance, attr, validated_item)
        instance.save()
        return instance


class PublicUserSerializer(serializers.ModelSerializer):
    """PublicUserSerializer used to define field that are public.

    ['mail', 'last_name', 'first_name']
    """

    class Meta(object):
        """The Meta class of the PublicUserSerializer."""

        model = User
        fields = (
            "mail",
            "last_name",
            "first_name",
        )
