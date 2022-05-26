from django import forms

from donate.models import Donation


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password2 = forms.CharField()


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'pick_up_date': forms.SelectDateWidget()}
