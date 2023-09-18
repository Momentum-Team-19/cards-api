from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followed_users = models.ManyToManyField(
        "self",
        through="FollowRelationship",
        related_name="followed_by",
        symmetrical=False,
    )

    def follow_another_user(self, other_user):
        relationship, created = FollowRelationship.objects.get_or_create(
            follower=self, followed_user=other_user
        )
        return relationship

    def unfollow_another_user(self, other_user):
        FollowRelationship.objects.filter(
            follower=self, followed_user=other_user
        ).delete()

    def block_follower(self, other_user):
        relationship = FollowRelationship.objects.get(
            follower=other_user, followed_user=self
        )
        relationship.status = FollowRelationship.Status.BLOCKED
        relationship.save()
        return relationship

    def unblock_follower(self, other_user):
        relationship = FollowRelationship.objects.get(
            follower=other_user, followed_user=self
        )
        relationship.status = FollowRelationship.Status.FOLLOWING
        relationship.save()
        return relationship

    def get_followed_users(self):
        return self.following.filter(status=FollowRelationship.Status.FOLLOWING)

    def get_followers(self):
        return self.followers.filter(status=FollowRelationship.Status.FOLLOWING)

    def get_users_blocking_me(self):
        return self.following.filter(status=FollowRelationship.Status.BLOCKED)

    def get_blocked_followers(self):
        return self.followers.filter(status=FollowRelationship.Status.BLOCKED)


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Card(BaseModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    front_text = models.CharField(max_length=255)
    back_text = models.CharField(max_length=255, null=True, blank=True)
    background_color = models.CharField(max_length=255)
    font = models.CharField(max_length=255, null=True, blank=True)
    draft = models.BooleanField(
        default=False
    )  # false because front end may not implemet draft feature

    def __str__(self):
        return f"Card: {self.front_text}"


class FollowRelationship(models.Model):
    class Status(models.IntegerChoices):
        FOLLOWING = (1, "Following")
        BLOCKED = (0, "Blocked")

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    status = models.IntegerField(choices=Status.choices, default=Status.FOLLOWING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed_user.username}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed_user"], name="unique_follows"
            )
        ]