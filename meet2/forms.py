from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminTimeWidget


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=150)
    
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
    DateTime = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), required=True)
    
    class Meta:
        model = Events
        fields = ('EventPlace','EventDescription','EventName','DateTime')

class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('GroupName', 'GroupDescription')       
        
class UserInterestedEventsForm(forms.ModelForm):
    EntryTime = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    ExitTime = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    class Meta:
        model = UserInterestedEvents
        fields = ('EntryTime','ExitTime',)

class PhoneForm(forms.Form):        
    PhoneNumber1 = forms.RegexField(regex=r'^[6-9]\d{9}$', help_text='[Phone number be 10 digit starting with 6,7,8 or 9]')
    PhoneNumber2 = forms.RegexField(required=False, regex=r'^[6-9]\d{9}$', help_text='(Optional)  [Phone number be 10 digit starting with 6,7,8 or 9]')                          