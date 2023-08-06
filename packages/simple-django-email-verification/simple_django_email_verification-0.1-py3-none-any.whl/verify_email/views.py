import logging

from django.http import Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.signing import SignatureExpired, BadSignature
from django.contrib.auth.views import FormView
from .app_configurations import GetFieldFromSettings
from .confirm import verify_user
from .email_handler import resend_verification_email
from .forms import RequestNewVerificationEmailForm
from .errors import (
    InvalidToken,
    MaxRetriesExceeded,
    UserAlreadyActive,
    UserNotFound,
)

logger = logging.getLogger(__name__)

pkg_configs = GetFieldFromSettings()

login_page = pkg_configs.get('login_page')

success_msg = pkg_configs.get('verification_success_msg')
failed_msg = pkg_configs.get('verification_failed_msg')

failed_template = pkg_configs.get('verification_failed_template')
success_template = pkg_configs.get('verification_success_template')
link_expired_template = pkg_configs.get('link_expired_template')
request_new_email_template = pkg_configs.get('request_new_email_template')
new_email_sent_template = pkg_configs.get('new_email_sent_template')


def verify_user_and_activate(request, useremail, usertoken):
    """
    A view function already implemented for you so you don't have to implement any function for verification
    as this function will be automatically be called when user clicks on verification link.

    verify the user's email and token and redirect'em accordingly.
    """

    try:
        verified = verify_user(useremail, usertoken)
        if verified is True:
            if login_page and not success_template:
                messages.success(request, success_msg)
                return redirect(to=login_page)
            return render(
                request,
                template_name=success_template,
                context={
                    'msg': success_msg,
                    'status': 'Verification Successful!',
                    'link': reverse(login_page)
                }
            )
        else:
            # we dont know what went wrong...
            raise ValueError
    except (ValueError, TypeError) as error:
        logger.error(f'[ERROR]: Something went wrong while verifying user, exception: {error}')
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': failed_msg,
                'minor_msg': 'There is something wrong with this link...',
                'status': 'Verification Failed!',
            }
        )
    except SignatureExpired:
        return render(
            request,
            template_name=link_expired_template,
            context={
                'msg': 'The link has lived its life :( Request a new one!',
                'status': 'Expired!',
                'encoded_email': useremail,
                'encoded_token': usertoken
            }
        )
    except BadSignature:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'This link was modified before verification.',
                'minor_msg': 'Cannot request another verification link with faulty link.',
                'status': 'Faulty Link Detected!',
            }
        )
    except MaxRetriesExceeded:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'You have exceeded the maximum verification requests! Contact admin.',
                'status': 'Maxed out!',
            }
        )
    except InvalidToken:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'This link is invalid or been used already, we cannot verify using this link.',
                'status': 'Invalid Link',
            }
        )
    except UserNotFound:
        raise Http404("404 User not found")


class RequestNewLink(FormView):
    """
        Need to account for errors when resending an email
        - User exists but is already activated
            - Dave: dave.oren91@gmail.com
        - User exists but is not already activated
            - test1: dvnt191@gmail.com
        - User does not exist
        """
    form_class = RequestNewVerificationEmailForm
    template_name = request_new_email_template
    success_url = '/verification/user/verify-email/request-new-link/'

    def __init__(self):
        super().__init__()
        self.form_context = {
            'form': RequestNewVerificationEmailForm(),
            "message": "<ul>"
                       "<li>A new verification email has been sent if:</li>"
                       "<ul class='tier_2_ul'>"
                       "<li>A user with the specified email exists.</li>"
                       "<li>The user's email has not already been verified.</li>"
                       "</ul>"
                       "</ul>"
        }

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        user_email = form.data.get('email')
        # try-except block to check if user exists
        try:
            inactive_user = get_user_model().objects.get(email=user_email)
            status = resend_verification_email(self.request, user_email, user=inactive_user, encoded=False)
        except ObjectDoesNotExist as e:
            return self.form_invalid(form)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        return render(self.request, request_new_email_template, self.form_context)

    def form_invalid(self, form):
        return render(self.request, request_new_email_template, self.form_context)

def request_new_link(request, useremail=None, usertoken=None):
    """
    Need to account for errors when resending an email
    - User exists but is already activated
    - User exists but is not already activated
    - User does not exist
    """
    try:
        if useremail is None or usertoken is None:
            # request came from re-request email page
            if request.method == 'POST':
                form = RequestNewVerificationEmail(request.POST)  # do not inflate data
                if form.is_valid():
                    form_data: dict = form.cleaned_data
                    email = form_data['email']

                    inactive_user = get_user_model().objects.get(email=email)
                    # Error message if user is already active
                    if inactive_user.is_active:
                        return render(
                            request,
                            template_name=request_new_email_template,
                            context={
                                'form': RequestNewVerificationEmailForm(),
                                "message": "<ul>"
                                           "<li>A new verification email has been sent if:<\li>\n"
                                           "<ul>"
                                           "<li>A user with the specified email exists.</li>\n"
                                           "<li>The user's email has not been verified."
                                           "</ul>"
                                           "</ul>",
                            }
                        )
                    else:
                        # resend email
                        status = resend_verification_email(request, email, user=inactive_user, encoded=False)
                        if status:
                            return render(
                                request,
                                template_name=request_new_email_template,
                                context={
                                    'form': RequestNewVerificationEmail(),
                                    "message": "<ul>"
                                               "<li>A new verification email has been sent if:</li>"
                                               "<ul class='tier_2_ul'>"
                                               "<li>A user with the specified email exists.</li>"
                                               "<li>The user's email has not already been verified.</li>"
                                               "</ul>"
                                               "</ul>"
                                }
                            )
                        else:
                            logger.error('something went wrong during sending email')
            else:
                form = RequestNewVerificationEmail()
            return render(
                request,
                template_name=request_new_email_template,
                context={'form': form}
            )
        else:
            # request came from  previously sent link
            status = resend_verification_email(request, useremail, token=usertoken)

        if status:
            return render(
                request,
                template_name=request_new_email_template,
                context={
                    'form': RequestNewVerificationEmail(),
                    "message": "A new verification email has been sent",
                }
            )
        else:
            messages.info(request, 'Something went wrong during sending email :(')
            logger.error('something went wrong during sending email')

    except ObjectDoesNotExist as error:
        messages.warning(request, 'User not found associated with given email!')
        logger.error(f'[ERROR]: User not found. exception: {error}')
        return HttpResponse(b"User Not Found - [ERROR]: User not found. exception: {error}", status=404)

    except MultipleObjectsReturned as error:
        logger.error(f'[ERROR]: Multiple users found. exception: {error}')
        return HttpResponse(b"Internal server error! - [ERROR]: Multiple users found. exception: {error}", status=500)

    except KeyError as error:
        logger.error(f'[ERROR]: Key error for email in your form: {error}')
        return HttpResponse(b"Internal server error! - [ERROR]: Key error for email in your form: {error}", status=500)

    except MaxRetriesExceeded as error:
        logger.error(f'[ERROR]: Maximum retries for link has been reached. exception: {error}')
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'You have exceeded the maximum verification requests! Contact admin.',
                'status': 'Maxed out!',
            }
        )
    except InvalidToken:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': 'This link is invalid or been used already, we cannot verify using this link.',
                'status': 'Invalid Link',
            }
        )
    except UserAlreadyActive:
        return render(
            request,
            template_name=failed_template,
            context={
                'msg': "This user's account is already active",
                'status': 'Already Verified!',
            }
        )
