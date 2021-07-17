from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def t_dashboard(request):
    user_type = request.session['user_type']
    context = {
        'user_type': user_type,
        'user': request.user,
    }
    return render(request, 'tenant/dashboard.html', context)