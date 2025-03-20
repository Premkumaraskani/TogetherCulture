from django.shortcuts import render
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def membership_view(request):
    return render(request,'membership.html')

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def save_membership_application(request):
    if request.method == "POST":
        try:
            body_unicode = request.body.decode("utf-8")
            logger.info("Request Body: %s", body_unicode)
            data = json.loads(body_unicode)

            plan = data.get("plan")
            responses = data.get("responses")
            if not plan or not responses:
                error_msg = "Missing plan or responses."
                logger.error(error_msg)
                return JsonResponse({"success": False, "error": error_msg}, status=400)
            
            # Use the logged-in user's membership_info field.
            user = request.user
            membership_data = user.membership_info or {}
            membership_data[plan] = responses
            user.membership_info = membership_data
            user.save()
            return JsonResponse({"success": True})
        except Exception as e:
            logger.exception("Error saving membership application:")
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)



