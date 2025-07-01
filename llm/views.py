from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .llm_utils import generate_answer
from .models import llm 
import json

@csrf_exempt
def chat(request):
    if request.method == "POST":
        body = json.loads(request.body)
        question = body.get("question")
        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)
        answer = generate_answer(question)
        llm_instance = llm(
                    qusetion=question,  
                    answer=answer
                )
        llm_instance.save()
        return JsonResponse({"answer": answer})