from django.contrib import admin
from django.urls import include, path
from rest_framework_extensions.routers import ExtendedDefaultRouter

from tutorial.quickstart import views
from tutorial.quickstart.router import SwitchDetailRouter
from tutorial.quickstart.views import UserTweetViewSet, UserFollowsViewSet, UserFollowersViewSet, FollowViewSet
switch_router = SwitchDetailRouter()

router = ExtendedDefaultRouter()
user_route = router.register(r'users', views.UserViewSet)
user_route.register('tweets', UserTweetViewSet, 'user-tweets', ['username'])
user_route.register('follows', UserFollowsViewSet, 'user-follows', ['username'])
user_route.register('followed', UserFollowersViewSet, 'user-followers', ['username'])
router.register(r'feed', views.FeedViewSet)

switch_router.register(r'follow', FollowViewSet)
router.register(r'tweets', views.TweetViewSet)

urlpatterns = [
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
