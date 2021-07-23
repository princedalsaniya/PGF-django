import cloudinary
from django.shortcuts import render
from accounts.models import Tenant
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def t_dashboard(request):
    user_type = request.session['user_type']
    user = request.user

    print(user)
    print(user.username)
    profilePublicID = getattr(Tenant.objects.get(user=user), 'profilePicID')
    print(profilePublicID)
    profilePic = cloudinary.CloudinaryImage(profilePublicID).build_url(width = 200, height = 200, crop = 'fill', gravity="face")
    print(profilePic)

    context = {
        'user_type': user_type,
        'user': user,
        'profilePic': profilePic,
    }

    return render(request, 'tenant/dashboard.html', context)