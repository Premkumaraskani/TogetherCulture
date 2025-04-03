from django.shortcuts import render
import json
from django.http import JsonResponse
from login.models import Users
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
# Create your views here.

def user_view(request):
    users = Users.objects.filter(is_superuser=False, account_type='guest').exclude(membership_info={})
    valid_users = [user for user in users if any(k in user.membership_info for k in [
        'key access holder', 'community holder', 'create workspace holder'
    ])]
    actioned_users = Users.objects.exclude(account_type__in=['guest', 'admin'])

    total_members = Users.objects.filter(is_superuser=False).count()
    active_members = Users.objects.filter(is_active=True, is_superuser=False).count()

    pending_members = len(valid_users)

    return render(request, 'users/user.html', {
        'users': valid_users,
        'actioned_users': actioned_users,
        'total_members': total_members,
        'active_members': active_members,
        'pending_members': pending_members,
    })

    # return render(request, 'users/user.html', {'users': valid_users,'actioned_users': actioned_users})




def dashboard_view(request):
    print(">>> USER VIEW HIT <<<")
    users = Users.objects.filter(is_superuser=False, account_type='guest')
    return render(request, 'users/user.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def approve_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    membership_info = user.membership_info or {}

    if "key access holder" in membership_info:
        user.account_type = "key access holder"
    elif "community holder" in membership_info:
        user.account_type = "community holder"
    elif "create workspace holder" in membership_info:
        user.account_type = "create workspace holder"
    else:
        messages.error(request, "No valid membership info found.")
        return redirect('user')

    user.save()
    messages.success(request, f"{user.username} approved as {user.account_type}.")
    return redirect('user')



@user_passes_test(lambda u: u.is_superuser)
def reject_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    user.is_active = False
    user.account_type = "Rejected"
    user.save()
    messages.success(request, f"{user.username} has been rejected.")
    return redirect('user')