# Generated by Django 2.1.2 on 2020-03-31 06:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('CommentId', models.AutoField(primary_key=True, serialize=False)),
                ('Content', models.TextField()),
                ('CommentTime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('EventId', models.AutoField(primary_key=True, serialize=False)),
                ('DateTime', models.DateField(blank=True, null=True)),
                ('EventPlace', models.CharField(max_length=60)),
                ('EventDescription', models.TextField()),
                ('EventName', models.CharField(max_length=60)),
                ('EventCreationTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('Organiser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('GroupId', models.AutoField(primary_key=True, serialize=False)),
                ('GroupDescription', models.TextField()),
                ('GroupName', models.CharField(max_length=60)),
                ('GroupCreationTime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Moderator', models.BooleanField(default=False)),
                ('NoofPosts', models.PositiveIntegerField(default=0)),
                ('NoofEvents', models.PositiveIntegerField(default=0)),
                ('GroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Group')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HasEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalParticipants', models.PositiveIntegerField(default=0)),
                ('EventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Events')),
                ('GroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Group')),
            ],
        ),
        migrations.CreateModel(
            name='HasPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GroupId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Group')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PhoneNumber', models.CharField(max_length=12)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('PostId', models.AutoField(primary_key=True, serialize=False)),
                ('Likes', models.PositiveSmallIntegerField(default=0)),
                ('PostDescription', models.TextField()),
                ('PostTime', models.DateTimeField(blank=True, null=True)),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AddressRoomNo', models.CharField(max_length=60)),
                ('AddressHall', models.CharField(max_length=60)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterestedEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EntryTime', models.TimeField(blank=True, null=True)),
                ('ExitTime', models.TimeField(blank=True, null=True)),
                ('EventId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Events')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPostLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsTrue', models.BooleanField(default=False)),
                ('PostId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Post')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hasposts',
            name='PostId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Post'),
        ),
        migrations.AddField(
            model_name='comments',
            name='PostId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meet2.Post'),
        ),
        migrations.AddField(
            model_name='comments',
            name='UserId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userpostlikes',
            unique_together={('UserId', 'PostId')},
        ),
        migrations.AlterUniqueTogether(
            name='userinterestedevents',
            unique_together={('UserId', 'EventId')},
        ),
        migrations.AlterUniqueTogether(
            name='phonenumber',
            unique_together={('UserId', 'PhoneNumber')},
        ),
        migrations.AlterUniqueTogether(
            name='hasposts',
            unique_together={('GroupId', 'PostId')},
        ),
        migrations.AlterUniqueTogether(
            name='hasevents',
            unique_together={('GroupId', 'EventId')},
        ),
        migrations.AlterUniqueTogether(
            name='groupmembers',
            unique_together={('UserId', 'GroupId')},
        ),
    ]
