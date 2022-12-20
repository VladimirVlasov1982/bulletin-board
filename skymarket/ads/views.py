from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import pagination, viewsets
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer, AdCreateSerializer, \
    CommentCreateSerializer
from ads.filters import AdTitleFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from ads.permissions import IsOwnerOrAdmin


class CommentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_query_param = "page"
    max_page_size = 1000


@extend_schema_view(
    list=extend_schema(
        summary="Список объявлений",
        description="Получает список всех объявлений"
    ),
    retrieve=extend_schema(
        summary="Объявление",
        description="Получает развернутую информацию по объявлению"
    ),
    create=extend_schema(
        summary="Создание объявления",
        description="Создает объявление"
    ),
    destroy=extend_schema(
        summary="Удаление объявления",
        description="Удаляет  объявление"
    ),
    update=extend_schema(
        summary="Обновление объявления",
        description="Обновляет поля объявления"
    ),
    partial_update=extend_schema(
        summary="Частичное обновление",
        description="Обновляет определенные поля объявления"
    ),
)
class AdViewSet(viewsets.ModelViewSet):
    """Содержит в себе все базовые API-методы для объявлений"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdTitleFilter
    queryset = Ad.objects.all()
    default_serializer = AdSerializer
    serializer_classes = {
        "retrieve": AdDetailSerializer,
        "create": AdCreateSerializer,
    }
    default_permission = [AllowAny()]
    permissions = {
        "retrieve": [IsAuthenticated()],
        "create": [IsAuthenticated()],
        "update": [IsOwnerOrAdmin()],
        "partial_update": [IsOwnerOrAdmin()],
        "destroy": [IsOwnerOrAdmin()],
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)


@extend_schema_view(
    list=extend_schema(
        summary="Список отзывов к объявлению",
        description="Получает список всех отзывов к объявлению"
    ),
    retrieve=extend_schema(
        summary="Получение отзыва",
        description="Получает отзыв по ID"
    ),
    create=extend_schema(
        summary="Создание отзыва",
        description="Создает отзыв к объявлению"
    ),
    destroy=extend_schema(
        summary="Удаление отзыва",
        description="Удаляет отзыв"
    ),
    update=extend_schema(
        deprecated=True
    ),
    partial_update=extend_schema(
        summary="Обновление отзыва",
        description="Обновляет отзыв"
    ),
)
class CommentViewSet(viewsets.ModelViewSet):
    """Содержит в себе все базовые API-методы для отзывов"""
    queryset = Comment.objects.all()
    serializer_default = CommentSerializer
    serializer_classes = {
        "create": CommentCreateSerializer,
    }

    default_permission = [AllowAny()]
    permissions = {
        "retrieve": [IsAuthenticated()],
        "create": [IsAuthenticated()],
        "update": [IsOwnerOrAdmin()],
        "partial_update": [IsOwnerOrAdmin()],
        "destroy": [IsOwnerOrAdmin()],
    }
    pagination_class = CommentPagination

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_default)

    def get_queryset(self, *args, **kwargs):
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, pk=ad_id)

        return self.queryset.filter(ad=ad)


class UserAdsListView(ListAPIView):
    """Возвращает все объявления текущего пользователя"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        self.queryset = self.queryset.filter(author_id=self.request.user.pk)
        return self.queryset
