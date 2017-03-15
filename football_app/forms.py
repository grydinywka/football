from django import forms
from django.contrib.auth.models import User
from football_app.models import Tournament, Command, Voting, VotingList


class CreateToutnamentForm(forms.Form):
    """doc str for CreateToutnamentForm"""
    users = forms.MultipleChoiceField(
        label='Users*',
        help_text="Choose Users",
        error_messages={'required': "Field Users is required"},
        choices = [(user.id, user) for user in User.objects.all()],
        widget=forms.SelectMultiple(attrs={'size': '5'})

    )


class UpdateTourUsersForm(forms.ModelForm):
    """doc str for CreateToutnamentForm"""

    class Meta:
        model = Tournament
        fields = ('contestants',)
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(UpdateTourUsersForm, self).__init__(*args, **kwargs)
        self.initial["contestants"] = kwargs['initial']['users_pk']
        # self.fields["users2"].queryset = User.objects.filter(id__in=[1,29])

    contestants = forms.MultipleChoiceField(
        label='Contestants*',
        help_text="Choose Contestants",
        error_messages={'required': "Field Contestants is required"},
        choices = [(contestant.id, contestant.get_full_name() or contestant) for contestant in User.objects.all()],
        widget=forms.SelectMultiple(attrs={'size': '10',
                                           'class': 'form-control'
                                           })
        # initial=User.objects.all()
    )

    # users2 = forms.ModelMultipleChoiceField(
    #     label='Users2#',
    #     queryset=User.objects.all(),
    #     widget=forms.Select(
    #     attrs={
    #         'placeholder': 'Users', 'class': 'form-control','size': '10'}),
    #     required=True
    # )


# class UpdateTourCommandForm(forms.ModelForm):
#     """doc str for UpdateTourCommandsForm"""
#
#     class Meta:
#         model = Tournament
#         fields = ('commands',)
#         exclude = ()
#
#     def __init__(self, *args, **kwargs):
#         super(UpdateTourCommandForm, self).__init__(*args, **kwargs)
#         self.initial["commands"] = kwargs['initial']['commands_pk']
#         choices = [(command.id, command) for command in Command.objects.filter(pk__in=self.initial["commands"])]
#         self.fields['commands']._set_choices(choices)
#         # print self.fields['commands']._get_choices()
#         # print dir(self.fields['commands']._set_choices)
#
#     commands = forms.MultipleChoiceField(
#         label='Commands',
#         help_text="Choose Commands",
#         error_messages={'required': "Field Users is required"},
#         # choices = [(command.id, command) for command in Command.objects.all()],
#         widget=forms.SelectMultiple(attrs={'size': '10',
#                                            'class': 'form-control'
#                                            })
#         # initial=User.objects.all()
#     )
#
#     # commands= None


class CreateTournCommandForm(forms.ModelForm):

    class Meta:
        model = Command
        fields = ('contestant1', 'contestant2')

    def __init__(self, *args, **kwargs):
        super(CreateTournCommandForm, self).__init__(*args, **kwargs)
        choices = [(contestant.id, contestant)
                   for contestant in kwargs['initial']['contestants']]
        self.fields['contestant1']._set_choices(choices)
        self.fields['contestant2']._set_choices(choices)

    def clean(self, value=None):
        form_data = self.cleaned_data
        contestant1 = form_data['contestant1']
        contestant2 = form_data['contestant2']
        if contestant1 == contestant2:
            # print self._errors
            self._errors["contestant1"] = ["Check the contestant"]
            self._errors["contestant2"] = ["Check the contestant"]
            raise forms.ValidationError('You chosen the same contestant twice!')
        return self.cleaned_data


class ChampionshipGamesGenerateForm(forms.Form):
    """doc str for ChampionshipRoundGenerateForm"""
    amount = forms.IntegerField(
        max_value=5,
        min_value=1,
        label='Amount',
        help_text="Type amount of games which every command will play with every other command of the tournament",
        error_messages={'required': "Field Amount is required"},
    )


# class VotingCreateForm(forms.ModelForm):
#     """doc str for VotingCreateForm"""
#     class Meta:
#         model = VotingList
#         fields = ('tournament',)
