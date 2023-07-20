from django import forms
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize the form fields or labels here
        self.fields['old_password'].label = 'Current Password'
        self.fields['old_password'].widget.attrs = {'class': 'form-control','type': 'pasword'}
        self.fields['new_password1'].label = 'New Password'
        self.fields['new_password1'].widget.attrs = {'class': 'form-control','type': 'pasword'}
        self.fields['new_password2'].label = 'Confirm New Password'
        self.fields['new_password2'].widget.attrs = {'class': 'form-control','type': 'pasword'}


class CustomEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}),
    )

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use the custom email form instead of the default "email" field
        self.fields = CustomEmailForm().fields

        # Remove the label for the email field
        self.fields['email'].label = ''









        

        

