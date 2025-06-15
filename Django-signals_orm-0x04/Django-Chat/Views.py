from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")  # Or wherever you want to redirect
    return HttpResponseForbidden("You are not allowed to access this page.")
