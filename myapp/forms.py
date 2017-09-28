from django import forms


class PasswordResetForm(forms.Form):
    new_password = forms.CharField()
    # todo hide these fields from the user
    uid = forms.CharField(max_length=200)
    token = forms.CharField(max_length=200)
