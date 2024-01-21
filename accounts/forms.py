from django import forms
from .models import User, UserProfile


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["email"].widget.attrs["placeholder"] = "Email Address"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "address_line_1",
            "address_line_2",
            "city",
            "pin_code",
            "state",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["address_line_1"].widget.attrs["placeholder"] = "Address Line 1"
        self.fields["address_line_2"].widget.attrs["placeholder"] = "Address Line 2"
        self.fields["city"].widget.attrs["placeholder"] = "City"
        self.fields["pin_code"].widget.attrs["placeholder"] = "Pin Code"
        self.fields["state"].widget.attrs["placeholder"] = "State"
        self.fields["country"].widget.attrs["placeholder"] = "Country"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
