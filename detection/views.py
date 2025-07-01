import os
import uuid
import datetime
from shutil import copy2
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO
from pathlib import Path
from django.shortcuts import render
from .models import detection  

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
def detection_view(request): 
    if request.method == "GET":
        return render(request, "detection.html")

    if request.method == "POST" and request.FILES.get("image"):
        uploaded_file = request.FILES["image"]

        if uploaded_file and allowed_file(uploaded_file.name):
            try:
                uploads_dir = os.path.join(settings.STATIC_ROOT, "uploads")
                Path(uploads_dir).mkdir(parents=True, exist_ok=True)

             
                unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
                uploaded_file_path = os.path.join(uploads_dir, unique_filename)

                
                with open(uploaded_file_path, 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)

                model = YOLO(os.path.join(settings.BASE_DIR, "static", "yolo_model", "best.pt"))

                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_output_dir = f"detected_{timestamp}"
                runs_dir = os.path.join(settings.STATIC_ROOT, "runs")
                Path(runs_dir).mkdir(parents=True, exist_ok=True)

                results = model.predict(
                    source=uploaded_file_path,
                    imgsz=640,
                    conf=0.2,
                    save=True,
                    project=runs_dir,
                    name=unique_output_dir
                )
                class_names = [results[0].names[int(idx)] for idx in results[0].boxes.cls]
                
                yolo_output_dir = os.path.join(runs_dir, unique_output_dir)
                processed_image_path = next(Path(yolo_output_dir).glob("*.jpg"), None) 
                if processed_image_path is None:
                    raise Exception("Processed image not found")

                
                media_detection_dir = os.path.join(settings.MEDIA_ROOT, "detection/Images")
                Path(media_detection_dir).mkdir(parents=True, exist_ok=True)

               
                final_image_name = f"{uuid.uuid4()}_{processed_image_path.name}"
                final_image_path = os.path.join(media_detection_dir, final_image_name)

                
                copy2(processed_image_path, final_image_path)
                if not class_names:
                    d_name = "Not Found "
                else:
                    d_name = class_names[0] 

                detection_instance = detection(
                    diseases=d_name,  
                    image=f"detection/Images/{final_image_name}"
                )
                detection_instance.save()

                detections = []
                for result in results: 
                    for box in result.boxes:
                        detections.append({
                            "xmin": box.xyxy[0][0].item(),
                            "ymin": box.xyxy[0][1].item(),
                            "xmax": box.xyxy[0][2].item(),
                            "ymax": box.xyxy[0][3].item(),
                            "confidence": box.conf[0].item(),
                            "class_id": box.cls[0].item(),
                            "class_name": result.names[int(box.cls[0].item())],
                        })

                return JsonResponse({
                    "message": "Image processed successfully",
                    "output_image_url": f"{settings.MEDIA_URL}detection/Images/{final_image_name}",
                    "detections": detections
                }, status=200)

            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

        else:
            return JsonResponse({"error": "File type not allowed"}, status=400)

    else:
        return JsonResponse({"error": "No image file provided"}, status=400)
