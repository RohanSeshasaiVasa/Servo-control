import requests
from django.http import JsonResponse
from django.shortcuts import render

PI_IP = "http://192.168.0.250:5000"  # Replace with your Pi's IP

def index(request):
    return render(request, 'control/index.html')

def move_servo(request):
    angle = int(request.GET.get('angle', 90))
    try:
        r = requests.get(f"{PI_IP}/servo", params={"angle": angle}, timeout=1)
        data = r.json()
    except Exception as e:
        data = {"status": "error", "message": str(e)}
    return JsonResponse(data)
