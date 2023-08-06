from django import forms
from django.contrib.auth import get_user_model


class RequestNewVerificationEmailForm(forms.Form):
    email = forms.EmailField(
        label=get_user_model()._meta.get_field("email").verbose_name,  # noqa
        help_text=get_user_model()._meta.get_field("email").help_text,  # noqa
    )
