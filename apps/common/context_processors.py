from django.urls import resolve

#con esto Django detecte automáticamente la app de la URL actual y la pase a los templates
#esto porque usamos archivos css, js, etc globales y ademas algunos en cada app

def app_name_context(request):
    try:
        app_name = resolve(request.path).app_name
    except:
        app_name = None
    return {'current_app': app_name}
