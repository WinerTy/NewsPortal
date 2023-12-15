from django.contrib.auth.decorators import login_required
from django.shortcuts import render




@login_required
class ProfileView():
    def profile(request):
        return render(request, 'avtorization/profile.html')
