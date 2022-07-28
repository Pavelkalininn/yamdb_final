import datetime

from django.contrib.auth import authenticate
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (CODE_LENGTH, Category, Comment, Genre, Review,
                            Title, User)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = 'name', 'slug'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'name', 'slug'
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=True)
    description = serializers.CharField(
        required=False
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, year):
        if (1000 > year
                or year > datetime.datetime.now().year):
            raise serializers.ValidationError('Некорректно введен год')
        return year

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(score=Avg('score'))
        return rating.get('score')


class TitlePutSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        required=False,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        required=True,
        slug_field='slug'
    )

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')
        model = Title
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if value not in range(1, 11):
            raise serializers.ValidationError(
                'Оцените цифрой от 1 до 10'
            )
        return value

    def validate(self, obj):
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context.get('request').user
        title = get_object_or_404(Title, id=title_id)
        if self.context.get('request').method != 'PATCH':
            if title.reviews.filter(author=author).exists():
                raise serializers.ValidationError(
                    'Ваш отзыв уже есть.'
                )
        return obj


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    pub_date = serializers.DateTimeField(
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class SignUpSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(
        max_length=CODE_LENGTH,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'confirmation_code')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Сочетание "me" нельзя использовать в качестве никнейма.'
            )
        return username

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.email_user(
            subject='confirmation_code',
            message=user.confirmation_code,
            fail_silently=False
        )
        return {
            'email': user.email,
            'username': user.username,
        }


class TokenSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }
        confirm_code = None
        if 'request' in self.context:
            authenticate_kwargs['request'] = self.context['request']
            confirm_code = self.context['request'].data['confirmation_code']

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            raise NotFound(
                'User does not exist.'
            )

        if self.user.confirmation_code != confirm_code:
            raise serializers.ValidationError(
                'Invalid confirmation_code.'
            )

        access = AccessToken.for_user(self.user)

        return {
            'token': str(access)
        }


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )
