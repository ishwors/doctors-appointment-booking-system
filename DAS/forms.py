from django.contrib.auth.forms import PasswordChangeForm

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


        

        

