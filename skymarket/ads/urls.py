from django.urls import include, path

# TODO настройка роутов для модели
from rest_framework.routers import SimpleRouter

from ads.views import AdViewSet, CommentViewSet, UserAdsListView
from rest_framework_nested.routers import NestedSimpleRouter

ad_router = SimpleRouter()
ad_router.register("ads", AdViewSet)

comment_router = NestedSimpleRouter(
    ad_router,
    "ads",
    lookup="ad"
)

comment_router.register("comments", CommentViewSet)

urlpatterns = [
    path("", include(ad_router.urls)),
    path("", include(comment_router.urls)),

]
