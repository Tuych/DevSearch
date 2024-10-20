from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.forms import ModelForm


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # tepadagi classga boglandi

        for field in self.fields.values():  # fields lstnini forlayabmiz
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'  # __all__ hamma columnni oladi
        exclude = ['owner']  # eclude da formaga qushilmaydigan columnlar yozib quyiladi

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # tepadagi classga boglandi

        for field in self.fields.values():  # fields lstnini forlayabmiz
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_youtube',
                  'social_website']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # tepadagi classga boglandi

        for field in self.fields.values():  # fields lstnini forlayabmiz
            field.widget.attrs.update({'class': 'input'})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        label = {'first_name': 'Name'}  # html sahifada first_name Name bulib kurinsin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # tepadagi classga boglandi

        for field in self.fields.values():  # fields lstnini forlayabmiz
            field.widget.attrs.update({'class': 'input'})
