from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, RegisteredEvent

@login_required
def events_view(request):
    events = Event.objects.all()
    registered_events = RegisteredEvent.objects.filter(username=request.user)
    registered_event_ids = registered_events.values_list('event_id', flat=True)
    available_events = events.exclude(id__in=registered_event_ids)

    return render(request, 'events/eventspage.html', {
        'events': events,
        'registered_events': registered_events,
        'registered_event_ids': registered_event_ids,  # Pass registered event IDs to the template
        'access_types': Event.ACCESS_CHOICES,
    })

@login_required
def add_event(request):
    if request.method == "POST":
        print("Incoming POST data:", request.POST)  # Debugging: Log incoming data
        eventname = request.POST.get("eventname")
        date = request.POST.get("date")
        description = request.POST.get("description")
        access_by = request.POST.get("access_by")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        # Validate required fields
        if not eventname:
            return JsonResponse({"error": "Event name is required."}, status=400)
        if not date:
            return JsonResponse({"error": "Event date is required."}, status=400)
        if not description:
            return JsonResponse({"error": "Event description is required."}, status=400)
        if not access_by:
            return JsonResponse({"error": "Access type is required."}, status=400)

        # Validate access_by
        valid_access_types = [choice[0] for choice in Event.ACCESS_CHOICES]
        if access_by not in valid_access_types:
            return JsonResponse({"error": "Invalid access type selected."}, status=400)

        # Create the event
        try:
            Event.objects.create(
                eventname=eventname,
                date=date,
                description=description,
                access_by=access_by,
                location=location,
                image=image,
                created_by=request.user
            )
            return JsonResponse({"message": "Event created successfully!"}, status=201)
        except Exception as e:
            print("Error while creating event:", e)  # Debugging: Log the error
            return JsonResponse({"error": "An error occurred while creating the event."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
@login_required
def register_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_id = data.get("event_id")
            event = Event.objects.get(id=event_id)

            # Check if the user is eligible to register
            user_account_type = request.user.get_account_type_display()
            event_access_type = event.get_access_by_display()
            if user_account_type != event_access_type:
                return JsonResponse({"error": "You are not eligible to register for this event."}, status=403)

            # Check if the user is already registered
            if RegisteredEvent.objects.filter(username=request.user, event=event).exists():
                return JsonResponse({"error": "You are already registered for this event."}, status=400)

            # Register the user for the event
            RegisteredEvent.objects.create(username=request.user, event=event)
            return JsonResponse({"message": "Successfully registered for the event!"}, status=201)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def edit_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id, created_by=request.user)
        event.eventname = request.POST.get('eventname', event.eventname)
        event.date = request.POST.get('date', event.date)
        event.description = request.POST.get('description', event.description)
        event.access_by = request.POST.get('access_by', event.access_by)
        event.location = request.POST.get('location', event.location)

        if 'image' in request.FILES:
            event.image = request.FILES['image']

        event.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)