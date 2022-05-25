from datetime import datetime

from django import forms

from donate.models import Institution, User, Donation


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    name = forms.CharField()
    surname = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password2 = forms.CharField()


# class DonationForm(forms.Form):
#     quantity = forms.IntegerField()
#     institution = forms.ModelChoiceField(queryset=Institution.objects.all())
#     phone_number = forms.IntegerField()
#     city = forms.CharField(max_length=20)
#     zip_code = forms.IntegerField()
#     pick_up_date = forms.DateField()
#     pick_up_time = forms.TimeField()
#     pick_up_comment = forms.CharField(widget=forms.Textarea)
#     user = forms.ModelChoiceField(queryset=User.objects.all())

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
        exclude = ['user', 'categories']
        widgets = {
            'pick_up_date': forms.SelectDateWidget()}
