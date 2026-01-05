from django.http import HttpResponse
from django.template import loader

def cooking_suggestion(request):
  template = loader.get_template('fridge_photo_upload.html')
  return HttpResponse(template.render())