from django.shortcuts import render, HttpResponse, reverse, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant, Owner
from django.contrib.auth.models import User

#for sending the verification mails.
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import token_generator
from django.template.loader import render_to_string

# Create your views here.
def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            cd = login_form.cleaned_data
            username, password, user_type = cd.get('username'), cd.get('password'), cd.get('user_type')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    request.session['user_type'] = user_type

                    # Other way around
                    if user_type == 'Tenant':
                        tenant = Tenant.objects.filter(user=user)
                        if tenant:
                            login(request, user)
                            request.session['tenant'] = tenant[0]
                            return render(request, 'tenant/dashboard.html')
                        else:
                            messages.add_message(request, messages.ERROR, "You have chose wrong user type.")
                            return render(request, 'accounts/login_fail.html')
                    elif user_type == 'PG Owner':
                        owner = Owner.objects.filter(user=user)
                        if owner:
                            login(request, user)
                            return HttpResponse('your owner id is : ', owner)
                        else:
                            messages.add_message(request, messages.ERROR, "You have chose wrong user type.")
                            return render(request, 'accounts/login_fail.html')
                    elif user_type == 'Admin':
                        if user.is_superuser:
                            login(request, user)
                            return HttpResponse('Welcome Admin...')
                        else:
                            messages.add_message(request, messages.ERROR, "You have chose wrong user type.")
                            return render(request, 'accounts/login_fail.html')
                else:
                    messages.add_message(request, messages.ERROR, "Your Account is not Active. Please check your Emails. We have previously sent you an activation Link.")
                    return render(request, 'accounts/login_fail.html')
            else:
                messages.add_message(request, messages.ERROR,
                                     "Sorry, Username and Password didn't matched.")
                return render(request, 'accounts/login_fail.html')
        else:
            messages.add_message(request, messages.ERROR,
                                 "Your form is invalid. So, you have probably made a mistake in filling the form. So, please fill the form again.")
            return render(request, 'accounts/login_fail.html')

    login_form = LoginForm()
    return render(request, 'accounts/login.html', {'login_form': login_form})

def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def signup(request):

    if request.method == 'POST':
        context = {'has_error': False}
        s_form = SignUpForm(request.POST)
        if s_form.is_valid:
            username = request.POST.get('username')
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            email = request.POST.get('email')
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')

            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, "Username is already taken.")
                context['has_error'] = True
            elif User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, "Email is already registered.")
                context['has_error'] = True
            elif pwd1 != pwd2:
                messages.add_message(request, messages.ERROR, "Password and Repeat Password didn't matched.")
                context['has_error'] = True
            else:
                new_user = s_form.save(commit=False)
                new_user.is_active = False
                request.session['newuser'] = new_user
                new_user.set_password(pwd1)
                new_user.save()

                #sending email
                uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
                domain = get_current_site(request).domain
                # link = reverse('verfiyEmail', kwargs={'uidb64': uidb64, })
                email_subject = "Email verification for PGF account."
                message = render_to_string(
                    './accounts/email_verification_body.html',
                    {
                        'user': new_user,
                        'domain': domain,
                        'uid': uidb64,
                        'token': token_generator.make_token(new_user),
                    }
                )
                email = EmailMessage(
                    email_subject,
                    message,
                    'noreply@pgf.com',
                    [email],
                )
                email.send(fail_silently=False)
                return render(request, 'accounts/email_sent.html', {'new_user': new_user})
        else:
            messages.add_message(request, messages.ERROR, "You might have made mistake in filling the form. So, please try again.")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'accounts/signup_fail.html', context)

    signup_form = SignUpForm()
    return render(request, 'accounts/signup.html', {'signup_form': signup_form})

def verfy_email(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user.is_active:
        messages.add_message(request, messages.ERROR, "Your email is already verified. So, Don't try to do that again.")
        return render(request, 'accounts/email_verified_fail.html')

    elif user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/email_verified.html')

    messages.add_message(request, messages.ERROR, "Ooohhh!! error occurred during your Email Verification.")
    return render(request, 'accounts/email_verified_fail.html')