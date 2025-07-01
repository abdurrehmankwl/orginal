from django.shortcuts import render
from django.http import JsonResponse
from home.models import Contact
from django.views.decorators.csrf import csrf_exempt 
import json

@csrf_exempt
def contactUS(request):
    if request.method == "POST":
            try:
                data = json.loads(request.body)
                name = data.get("name")  
                email = data.get("email")
                message = data.get("message")
                if name and email and message :
                    contactData = Contact(name =name ,email = email , message = message)
                    contactData.save()
                    return JsonResponse({"message": "Thanks for Contacting US"}, status=200)
                else:
                    return JsonResponse({"message": "Empty Message"}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)

        
