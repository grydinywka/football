from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    """doc str for UserForm"""
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name',]

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        print "wserwserserserserserserserserseres"
        return super(UserForm, self).clean()
