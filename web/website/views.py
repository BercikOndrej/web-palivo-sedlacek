from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from . import models
import csv
import os

# Create your views here.
def index(request):
  if request.method == "POST":
    name = request.POST["first-name"] + " " + request.POST["last-name"]
    email = request.POST["email"]
    phone_number = request.POST["phone-number"]
    subject = request.POST["subject"]
    message = request.POST["message"]

    message = message + "\n \n \nZprávu poslala osoba jménem \"" + name + "\" pomocí kontaktního formuláře umístěného na webu \"palivosedlacek.cz\".\n \n"+ "Kontaktní údaje:\nTel: " + phone_number + "\nemail: " + email 
    
    success = send_mail(
      subject,
      message,
      email,
      [settings.EMAIL_HOST_USER],
      fail_silently=False
    )
    # send_email fun return 1 if was successful
    if success != 1:
      success = 0
    
    items = get_wood_item_from_csv()
    context = {
      "success": success,
      "wood_items": items
    }
    return render(request, 'website/index.html', context)
  else:
    items = get_wood_item_from_csv()
    return render(request, 'website/index.html', {"wood_items": items} )
  

def get_wood_item_from_csv(): 
  """Provides data from static csv file about wood items for price list"""
  wood_items = []
  file_path = os.environ.get('CSV_FILE_PATH')

  with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        line_count+= 1
      else:
        item = models.WoodItem(row[1], row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        wood_items.append(item)
        line_count+= 1
  return wood_items

@require_GET
def robots_txt(request):
  robots_txt_content = """\
  User-Agent: * 
  Allow: / 
  """
  return HttpResponse(robots_txt_content, content_type="text/plain")