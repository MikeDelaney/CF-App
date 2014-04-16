from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(label="First Name:", required=True)
	last_name = forms.CharField(label="Last Name:", required=False)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		if commit:
			user.save()
			g = Group.objects.get(name='std_user')
			g.user_set.add(user)
		return user


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", max_length=30, required=True)
    last_name = forms.CharField(label="Last name", max_length=30, required=False)
    email = forms.EmailField(label="E-mail Address")
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput, required=False)
 

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


	def __init__(self, *args, **kwargs):
		super(UserEditForm, self).__init__(*args, **kwargs)


    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
 
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        else:
            if len(password2) > 0 and len(password2) < 8:
                raise forms.ValidationError("Your password must be a minimum of 8 characters.")
        return password2
 
    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        if len(self.cleaned_data['new_password2']) > 0:
            user.set_password(self.cleaned_data['new_password2'])
        if commit:
            user.save()
        return user
