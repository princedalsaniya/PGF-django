from django.shortcuts import render, HttpResponse, reverse, redirect
from .forms import LoginForm, SignUpForm, createTenantProfileForm, createOwnerProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant, Owner
from django.contrib.auth.models import User

#for sending the verification mails.
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import token_generator
from django.template.loader import render_to_string

#for photos stuff.
import cloudinary

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

                    # when user_type is "TENANT"
                    if user_type == 'Tenant':
                        tenant = Tenant.objects.filter(user=user)
                        if tenant:
                            login(request, user)
                            request.session['tenant_id'] = getattr(tenant[0], 'tenantID')
                            return redirect('t_dashboard')
                        else:
                            messages.add_message(request, messages.ERROR, "You have chose wrong user type.")
                            return render(request, 'accounts/login_fail.html')

                    # when user_type is "OWNER"
                    elif user_type == 'Owner':
                        owner = Owner.objects.filter(user=user)
                        if owner:
                            login(request, user)
                            request.session['owner_id'] = getattr(owner[0], 'ownerID')
                            return redirect('o_dashboard')
                        else:
                            messages.add_message(request, messages.ERROR, "You have chose wrong user type.")
                            return render(request, 'accounts/login_fail.html')

                    # when user_type is "ADMIN"
                    elif user_type == 'Admin':
                        if user.is_superuser:
                            login(request, user)
                            return HttpResponse("Welcome Admin.")
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

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def signup(request):

    if request.method == 'POST':
        context = {'has_error': False}
        s_form = SignUpForm(request.POST)

        if s_form.is_valid:
            username = request.POST.get('username')
            email = request.POST.get('email')
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            type = request.POST.get('type')

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
                new_user.set_password(pwd1)
                new_user.save()
                request.session['new_user_id'] = getattr(new_user, "id")
                request.session['new_user_type'] = type

                #sending email
                uidb64 = urlsafe_base64_encode(force_bytes(getattr(new_user, 'id')))
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
                return render(request, 'accounts/email_sent.html')
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
        user = User.objects.get(id=uid)

    except Exception as e:
        user = None

    if user.is_active:
        messages.add_message(request, messages.ERROR, "Your email is already verified. So, Don't try to do that again.")
        return render(request, 'accounts/email_verified_fail.html')

    elif user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'accounts/email_verified.html', {'type': request.session['new_user_type']})

    messages.add_message(request, messages.ERROR, "Ooohhh!! error occurred during your Email Verification.")
    return render(request, 'accounts/email_verified_fail.html')

def set_tenant(request):
    type = request.session['new_user_type']

    if type == 'Tenant':
        
        pid = get_next_tenantID()
        profilePicID = makePID(pid)

        if request.method == 'POST':
            profile_form = createTenantProfileForm(request.POST)
        
            if profile_form.is_valid:

                user = User.objects.get(id=request.session['new_user_id'])
                phone = request.POST.get('phone')
                workplace = request.POST.get('workplace')
                adharNo = request.POST.get('adharNo')
                bdate = request.POST.get('bdate')


                new_tenant = Tenant(user=user, tenantID=pid, phone=phone, workplace=workplace, adharNo=adharNo, bdate=bdate, profilePicID=profilePicID)
                new_tenant.save()
                context = {
                    'fname': getattr(user, 'first_name'),
                    'profielPic': cloudinary.CloudinaryImage(profilePicID).build_url(width = 200, height = 200, crop = 'fill', gravity="face")
                }
                return render(request, './accounts/set_profile_done.html', context)

        profile_form = createTenantProfileForm()
        return render(request, './accounts/set_profile.html', {'profile_form': profile_form, 'pid': profilePicID, 'type': 'Tenant'})

def set_owner(request):
    type = request.session['new_user_type']

    if type == 'Owner':
        
        oid = get_next_ownerID()
        profilePicID = makePID(oid)

        if request.method == 'POST':
        
            profile_form = createOwnerProfileForm(request.POST)
    
            print(request.session['new_user_id'])

            if profile_form.is_valid:
                print("The form is valid")

                user = User.objects.get(id=request.session['new_user_id'])
                phone = request.POST.get('phone')
                adharNo = request.POST.get('adharNo')

                new_tenant = Owner(user=user, ownerID=oid, phone=phone, adharNo=adharNo, profilePicID=profilePicID)
                new_tenant.save()
                context = {
                    'fname': getattr(user, 'first_name'),
                    'profielPic': cloudinary.CloudinaryImage(profilePicID).build_url(width = 200, height = 200, crop = 'fill', gravity="face")
                }
                return render(request, './accounts/set_profile_done.html', context)

        profile_form = createOwnerProfileForm()
        return render(request, './accounts/set_profile.html', {'profile_form': profile_form, 'pid': profilePicID, 'type': 'Owner'})

#Utility Functions
def get_next_tenantID():
    id = 1
    lastTenant = Tenant.objects.all().last()
    if lastTenant:
        id = int(getattr(lastTenant, 'tenantID')[1:])+1
        nextPID = "t" + str(id)
        return nextPID
    nextPID = "t" + str(id)
    return nextPID

def get_next_ownerID():
    id = 1
    lastOwner = Owner.objects.all().last()
    if lastOwner:
        id = int(getattr(lastOwner, 'ownerID')[1:])+1
        nextPID = "o" + str(id)
        return nextPID
    nextPID = "o" + str(id)
    return nextPID

def makePID(id):
    return "PGF/Profiles/"+id