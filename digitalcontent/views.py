from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import DigitalContent, RegisteredContent
from .forms import DigitalContentForm  # Import the form for creating digital content
from login.models import Users  # Import the Users model

def digital_view(request):
    # Fetch all digital content
    digital_contents = DigitalContent.objects.all()

    # Handle form submission for registering digital content
    if request.method == "POST":
        content_id = request.POST.get("content_id")
        try:
            content = DigitalContent.objects.get(id=content_id)
            # Check if the user is already registered
            if not RegisteredContent.objects.filter(username=request.user, content=content).exists():
                # Register the user for the content
                RegisteredContent.objects.create(username=request.user, content=content)
        except DigitalContent.DoesNotExist:
            pass  # No need to handle this with messages since popups are used
        return redirect("digital")

    # Fetch registered content for the logged-in user
    registered_ids = []
    registered_contents = []
    if request.user.is_authenticated:
        registered_contents = RegisteredContent.objects.filter(username=request.user)
        registered_ids = [content.content.id for content in registered_contents]

    # Define allowed creators
    allowed_creators = ['create workspace holder', 'key access holder', 'admin']

    # Pass data to the template
    context = {
        'digital_contents': digital_contents,
        'registered_ids': registered_ids,
        'registered_contents': registered_contents,
        'allowed_creators': allowed_creators,
    }
    return render(request, 'digitalcontent/digital.html', context)

@login_required
def add_digital_content(request):
    if request.method == "POST":
        form = DigitalContentForm(request.POST, request.FILES)
        if form.is_valid():
            digital_content = form.save(commit=False)
            # Validate access_by based on user role
            if request.user.account_type.lower() == 'key access holder' and digital_content.access_by != 'key access holder':
                return redirect('digital')
            elif request.user.account_type.lower() == 'create workspace holder' and digital_content.access_by not in ['community holder', 'key access holder', 'create workspace holder']:
                return redirect('digital')
            # Save the content
            digital_content.created_by = request.user.username
            digital_content.save()
            return redirect('digital')
    else:
        form = DigitalContentForm()
    return render(request, 'digitalcontent/add_digital_content.html', {'form': form})

@login_required
def digital_content_details(request, content_id):
    # Fetch the digital content
    digital_content = get_object_or_404(DigitalContent, id=content_id)

    # Fetch registered users for the digital content
    registered_users = RegisteredContent.objects.filter(content=digital_content)

    # Pass data to the template
    context = {
        'digital_content': digital_content,
        'registered_users': registered_users,
    }
    return render(request, 'digitalcontent/digital_content_details.html', context)

def registered_users(request, content_id):
    registered_users = RegisteredContent.objects.filter(content_id=content_id).values(
        'username__username', 'registered_at'
    )
    data = [
        {
            'username': user['username__username'],
            'registered_at': user['registered_at'].strftime('%Y-%m-%d %H:%M:%S'),
        }
        for user in registered_users
    ]
    return JsonResponse(data, safe=False)

@login_required
def digital_content_monitor(request, content_id):
    # Fetch the digital content
    digital_content = get_object_or_404(DigitalContent, id=content_id, created_by=request.user.username)

    # Fetch registered users for the digital content
    registered_users = RegisteredContent.objects.filter(content=digital_content).select_related('username')

    # Prepare data for JSON response
    data = {
        'digital_content': {
            'id': digital_content.id,
            'name': digital_content.name,
            'description': digital_content.description,
            'access_by': digital_content.access_by,
            'image_url': digital_content.image.url if digital_content.image else "",
        },
        'registered_users': [
            {
                'username': user.username.username,  # Fetch the username from the Users model
                'registered_at': user.registered_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for user in registered_users
        ],
    }
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_POST
@login_required
def update_digital_content(request):
    # Update digital content details
    content_id = request.POST.get("content_id")
    name = request.POST.get("name")
    description = request.POST.get("description")
    access_by = request.POST.get("access_by")
    image = request.FILES.get("image")

    try:
        digital_content = DigitalContent.objects.get(id=content_id, created_by=request.user.username)
        digital_content.name = name
        digital_content.description = description
        digital_content.access_by = access_by
        if image:
            digital_content.image = image
        digital_content.save()
        return JsonResponse({"success": True, "message": "Digital content updated successfully."})
    except DigitalContent.DoesNotExist:
        return JsonResponse({"success": False, "message": "Digital content not found."})
