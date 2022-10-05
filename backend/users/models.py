from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Q

User = get_user_model()


class Follow(models.Model):
    """Модель для подписок на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        indexes = [
            models.Index(fields=['user', 'author'], name='user_author'),
        ]
        constraints = [
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='user_not_author'),
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            )
        ]
