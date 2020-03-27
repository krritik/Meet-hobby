from django.conf import settings
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    AddressRoomNo = models.CharField(max_length=60)
    AddressHall = models.CharField(max_length=60)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()    

class PhoneNumber(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    PhoneNumber = models.CharField(max_length=60)

    def __str__(self):
        return self.PhoneNumber

class Post(models.Model):
    PostId = models.AutoField(primary_key=True)
    Likes = models.PositiveSmallIntegerField(default=0)
    PostDescription = models.TextField()
    PostTime = models.DateTimeField(blank=True, null=True)
    PostCreationTime = models.DateTimeField(default=timezone.now)
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)

    def publish(self):
        self.PostTime = timezone.now()
        self.save()    


class Comments(models.Model):
    CommentId = models.AutoField(primary_key=True)
    PostId = models.ForeignKey('Post',on_delete=models.CASCADE)
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    Content = models.TextField()
    CommentTime = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.CommentTime = timezone.now()
        self.save()

class Group(models.Model):
    GroupId = models.AutoField(primary_key=True)
    GroupDescription = models.TextField()
    GroupName = models.CharField(max_length=60)
    GroupCreationTime = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.GroupCreationTime = timezone.now()
        self.save()

    def __str__(self):
        return self.GroupName    

class Events(models.Model):
    EventId = models.AutoField(primary_key=True)
    DateTime = models.DateTimeField(blank=True, null=True)
    EventPlace = models.CharField(max_length=60)
    EventDescription = models.TextField()
    EventName = models.CharField(max_length=60)
    EventCreationTime = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.EventCreationTime = timezone.now()
        self.save()

    def __str__(self):
        return self.EventName

class HasEvents(models.Model):
    EventId = models.ForeignKey('Events',on_delete=models.CASCADE)
    GroupId = models.ForeignKey('Group',on_delete=models.CASCADE)
    TotalParticipants = models.PositiveIntegerField(default=0)

class HasPosts(models.Model):
    PostId = models.ForeignKey('Post',on_delete=models.CASCADE)
    GroupId = models.ForeignKey('Group',on_delete=models.CASCADE)

class UserInterestedEvents(models.Model):
    EventId = models.ForeignKey('Events',on_delete=models.CASCADE)
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    EntryTime = models.DateTimeField(blank=True, null=True)
    ExitTime = models.DateTimeField(blank=True, null=True)
    Organiser = models.CharField(max_length=60)

class GroupMembers(models.Model):
    UserId = models.ForeignKey(User,on_delete=models.CASCADE)
    GroupId = models.ForeignKey('Group',on_delete=models.CASCADE)
    Moderator = models.BooleanField(default=False)
    NoofPosts = models.PositiveIntegerField(default=0)
    NoofEvents = models.PositiveIntegerField(default=0)


