from django.shortcuts import render

from myapp.forms import PasswordResetForm


def successful_reset(request):
    return render(request, 'reset_success.html')


def insert_new_password(request, uid, token):
    """
    User receives an email with a password reset link.
    The User is then redirected here where he inserts his new password
    The User is then redirected to 'auth/password/reset/confirm/'
    """
    print("uid " + uid)
    print("token " + token)
    form = PasswordResetForm()
    # grab the token and uid from the url and insert then into the form
    # before user inserts their new_password
    # todo insert uid and token
    # form.cleaned_data['uid'] = uid
    # form.cleaned_data['token'] = token
    # todo place a redirect to success page then to home page when user navigates to 'auth/password/reset/confirm/'
    return render(request, 'insert_new_password.html', {
        'form': form
    })


def hello(request):
    return render(request, 'index.html')