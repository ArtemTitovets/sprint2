from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import *


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddUser
        fields = ['email', 'phone', 'surname', 'name', 'patronymic',]


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Photo
        fields = ['data', 'title']


class MountSerializer(WritableNestedModelSerializer):
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    user = AddUserSerializer()
    coords = CoordsSerializer()
    level = LevelSerializer(allow_null=True)
    photo = PhotoSerializer(many=True)


    class Meta:
        model = Mount
        fields = ('user', 'beautyTitle', 'title', 'other_titles', 'connect', 'coords', 'level', 'photo', 'add_time', 'status')

    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        photo = validated_data.pop('photo')

        user, created = AddUser.objects.get_or_create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        mount = Mount.objects.create(**validated_data, user=user, coords=coords, level=level, status='new')

        for image in photo:
            data = image.pop('data')
            title = image.pop('title')
            Photo.objects.create(data=data, mount=mount, title=title)

        return mount


    def validate(self, value):

        user_data = value['user']

        if self.instance:
            if (user_data['email'] != self.instance.user.email or
                user_data['surname'] != self.instance.user.surname or
                user_data['name'] != self.instance.user.name or
                user_data['patronymic'] != self.instance.user.patronymic or
                user_data['phone'] != self.instance.user.phone):
                raise serializers.ValidationError()
        return value

