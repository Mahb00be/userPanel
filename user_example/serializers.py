from rest_framework import serializers
from .models import Doctor, UserPanel, User, Comment, VisitTime


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'firstname', 'lastname', 'medicalNumber', 'city', 'medicalExpertise',
                  'educationDegree', 'phone', 'address']


class UserPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPanel

        fields = ['user', 'favoriteDoctors', 'age', 'location']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # ['username', 'first_name', 'last_name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'doctor', 'text']


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitTime
        fields = '__all__'

