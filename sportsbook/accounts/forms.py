from django import forms
from .models import WebsiteUser

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "Enter email address"
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Enter username"
    }))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Set password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),
    )

    class Meta:
        model = WebsiteUser
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = WebsiteUser(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"]
        )
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
