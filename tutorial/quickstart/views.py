from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from tutorial.quickstart.models import Tweet, Followers
from tutorial.quickstart.permissions import IsTweetAuthorOrReadOnly
from tutorial.quickstart.serializers import UserSerializer, TweetSerializer, UserFollowsSerializer, \
    UserFollowersSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')  # сортировка по дате (- говорит, что в обратном порядке)
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [
        IsTweetAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UserFollowsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = UserFollowsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            follower__username=self.kwargs['parent_lookup_username']
        )


class UserFollowersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Followers.objects.all()
    serializer_class = UserFollowersSerializer

    def get_queryset(self):
        return self.queryset.filter(
            follows__username=self.kwargs['parent_lookup_username']
        )


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Followers.objects
    serializer_class = UserFollowsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follows = User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(follower=self.request.user, follows=follows)

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field],
        )


class UserTweetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FeedViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        return self.queryset.filter(
            author__followers__follower=self.request.user,
            #           author__followers__follower__username=self.request.user.username
        )
