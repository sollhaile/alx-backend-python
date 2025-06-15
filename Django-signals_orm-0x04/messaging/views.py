from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({'message': 'User account deleted successfully'})
