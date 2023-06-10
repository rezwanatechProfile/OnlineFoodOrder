from rest_framework import serializers
from .models import User, UserProfile



class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Mark password field as write-only

    def create(self, validated_data):
        # Create a new User object using the validated data
        return User.objects.create(**validated_data)


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#       model = UserProfile
#       fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'zip_code','latitude', 'longitude']