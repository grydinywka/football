from django import forms
from django.contrib.auth.models import User


class CreateToutnamentForm(forms.Form):
    """doc str for CreateToutnamentForm"""
    users = forms.MultipleChoiceField(
        label='Users*',
        help_text="Choose Users",
        error_messages={'required': "Field Users is required"},
        choices = [(user.id, user) for user in User.objects.all()]
    )
    # amount_games = forms.IntegerField(
    #     max_value=5,
    #     min_value=1,
    #     help_text="Number of games which every command should plays with every other one"
    # )
