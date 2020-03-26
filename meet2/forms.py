from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post,Comments,Events,UserInterestedEvents

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=60, help_text='Username')
    email = forms.EmailField(max_length=150, help_text='Email')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class ProfileForm(forms.Form):
    AddressRoomNo = forms.CharField(max_length=60)
    AddressHall = forms.CharField(max_length=60)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('PostDescription',)
    
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('Content',)        

class EventForm(forms.ModelForm):

    class Meta:
        model = Events
        fields = ('EventPlace','EventDescription','EventName',)
        
class UserInterestedEventsForm(forms.ModelForm):

    class Meta:
        model = UserInterestedEvents
        fields = ('EntryTime','ExitTime',)