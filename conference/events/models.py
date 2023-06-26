from django.db import models
from django.urls import reverse

# #CLASS EXAMPLE
# class Blog(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     #UPDATE MODELS, DON'T FORGET TO APPLY MIGRATIONS
#     answer = models.TextField(null=True)
#     question = models.TextField(null=True)
#     category = models.CharField(max_length=200,null=True)

#     def get_api_url(self):
#         return reverse("show_blog_detail", kwargs={"id": self.id})

#     def add_comment(self, content):
#         comment = Comment.objects.create(
#             blog=self,
#             content=content,
#         )
#         self.comments.add(comment)


class State(models.Model):
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.abbreviation}"

    class Meta:
        ordering = ("abbreviation",)  # Default ordering for State


class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    room_count = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.ForeignKey(
        State,
        related_name="+",  # do not create a related name on State
        on_delete=models.PROTECT,
    )
    # Pexels API
    image_url = models.URLField(null=True)

    def get_api_url(self):
        return reverse("api_show_location", kwargs={"id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Conference(models.Model):
    name = models.CharField(max_length=200)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    max_presentations = models.PositiveSmallIntegerField()
    max_attendees = models.PositiveIntegerField()
    location = models.ForeignKey(
        Location,
        related_name="conferences",
        on_delete=models.CASCADE,
    )
    # Open Weather API
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    weather = models.TextField(null=True)

    def get_api_url(self):
        return reverse("api_show_conference", kwargs={"id": self.id})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("starts", "name")
