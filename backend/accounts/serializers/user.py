from rest_framework import serializers
from accounts.models.user import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
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
        """ Méthode create custom qui supporte les post requêtes pour les mots de passe.
        """
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Méthode update custom qui supporte les put requêtes pour les mots de passe.
        """
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ("mail", "last_name", "first_name",)