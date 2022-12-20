from rest_framework import serializers
from ads.models import Ad, Comment
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объявлений
    """
    pk = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=150, required=True)
    price = serializers.IntegerField(required=True)
    image = serializers.ImageField()
    description = serializers.CharField(max_length=1500)

    class Meta:
        model = Ad
        fields = ["pk", "image", "title", "price", "description"]


class AdDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объявления
    """
    pk = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=150, required=True)
    price = serializers.IntegerField(required=True)
    phone = serializers.SerializerMethodField(method_name="get_phone")
    description = serializers.CharField(max_length=1500)
    image = serializers.ImageField()

    author_first_name = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="first_name",
        source="author",
        required=False,
    )
    author_last_name = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="last_name",
        source="author",
        required=False,
    )
    author_id = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="pk",
        source="author",
        required=False,
    )

    class Meta:
        model = Ad
        fields = ["title", "price", "phone", "author_first_name", "author_last_name", "author_id", "pk",
                  "image", "description"]

    def get_phone(self, obj):
        phone = str(obj.author.phone)
        return phone


class AdCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания объявления
    """

    class Meta:
        model = Ad
        fields = ["image", "title", "price", "description"]

    def create(self, validated_data):
        validated_data["author_id"] = self.context["request"].user.pk
        return super(AdCreateSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отзывов
    """
    pk = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=400, required=True)
    author_id = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        source="author",
        slug_field="pk",
    )
    created_at = serializers.DateTimeField()
    author_first_name = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        source="author",
        slug_field="first_name",
    )
    author_last_name = serializers.SlugRelatedField(
        required=False,
        queryset=User.objects.all(),
        source="author",
        slug_field="last_name",
    )
    author_image = serializers.ImageField(source="author.image")

    ad_id = serializers.SlugRelatedField(
        required=False,
        queryset=Ad.objects.all(),
        source="ad",
        slug_field="pk",
    )

    class Meta:
        model = Comment
        fields = ["pk", "text", "author_id", "created_at", "author_first_name", "author_last_name", "ad_id",
                  "author_image"]


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания отзывов
    """
    pk = serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=400)
    created_at = serializers.DateTimeField(required=False)
    author_first_name = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        source="author",
        slug_field="first_name",
        required=False,
    )
    author_last_name = serializers.SlugRelatedField(
        queryset=Ad.objects.all(),
        source="author",
        slug_field="last_name",
        required=False,
    )
    author_image = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="image",
        required=False,
    )

    class Meta:
        model = Comment
        fields = ["pk", "text", "author_id", "created_at", "author_first_name", "author_last_name", "ad_id",
                  "author_image"]

    def create(self, validated_data):
        validated_data["ad_id"] = self.context["view"].kwargs["ad_pk"]
        validated_data["author_id"] = self.context["request"].user.pk

        return super(CommentCreateSerializer, self).create(validated_data)
