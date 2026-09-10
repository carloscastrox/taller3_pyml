import os
import requests
from django.shortcuts import render


def home(request):
    context = {}
    
    if request.method == 'POST':
        area_m2 = request.POST.get('area_m2')
        
        if area_m2:
            try:
                # URL de tu API FastAPI
                api_url = os.environ.get("API_URL", "http://127.0.0.1:8000/predict")
                payload = {"area_m2": float(area_m2)}
                
                # Consumir la API
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    # Formatear el precio como moneda para que se vea mejor
                    precio_formateado = f"${data['predicted_price']:,.2f}"
                    context['resultado'] = precio_formateado
                    context['area'] = area_m2
                else:
                    context['error'] = "La API respondió con un error."
                    
            except requests.exceptions.RequestException as e:
                context['error'] = "No se pudo conectar con la API. ¿Está FastAPI corriendo?"

    return render(request, 'index.html', context)