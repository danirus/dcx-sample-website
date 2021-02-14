from django.template.response import TemplateResponse


def home_v(request):
    return TemplateResponse(request, 'homepage.html')