
from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.quickstart.models import Tweet, Followers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class TweetSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['url', 'id', 'text', 'photo', 'author', 'created']


class UserFollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer(read_only=True)

    class Meta:
        model = Followers
        fields = ['follows']


class UserFollowersSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Followers
        fields = ['follower', 'followed']

#  follows = SlugRelatedField('username')