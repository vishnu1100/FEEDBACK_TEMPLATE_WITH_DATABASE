from django.shortcuts import render,redirect
from .models import Feedback,login as log
from datetime import datetime
from django.core.mail import send_mail



import requests
from django.http import HttpResponse
from weddingvia.msg91config import MSG91_AUTH_KEY, MSG91_SENDER_ID

def login(request):
    return render(request,"login.html")

def login_form(request):
    if request.POST:
        user = request.POST["username"]
        password = request.POST["password"]
        try:
            datac = log.objects.filter(username=user, password=password).count()
            if datac==1:
              data=log.objects.get(username=user, password=password)
              if data.role=="staff":
                 request.session['username'] = data.username
                 request.session['role'] = data.role
                 request.session['id'] = data.logid
                 response=redirect('/table')
                 return response
              else:
                 response = redirect('/feedback_form?msg=invalid access')
                 return response
            else:
              response = redirect('/feedback_form?msg=invalid username or password')
              return response
        except:
            response = redirect('/feedback_form?msg=something went wrong')
            return response
    else:
        response = redirect('/feedback_form')
        return response

def send_email(recipient_email):
    
    url = 'https://api.msg91.com/api/v5/email/send'
    headers = {
        'authkey': MSG91_AUTH_KEY,
    }
    data = {
        'sender': MSG91_SENDER_ID,
         
        'to': [
        {
            'email': recipient_email # Replace with the recipient's email address
        }
        ],
        "from": {
             "email": "anandak@weddingvia.in"
         },  
        "domain":"weddingvia.in",
        "template_id":"ticket_created_final",
        "mail_type_id":"1",
        "variables":{
            "email":recipient_email
        }
        
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 200:
        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Email sending failed.')
    
def send_complaint(recipient_email):
    url = 'https://api.msg91.com/api/v5/email/send'
    headers = {
        'authkey': MSG91_AUTH_KEY,
    }
    data = {
        'sender': MSG91_SENDER_ID,
         
        'to': [
        {
            'email': recipient_email 
        }
        ],
        "from": {
             "email": "anandak@weddingvia.in"
         },  
        "domain":"weddingvia.in",
        "template_id":"ticket_resolved_final1",
        "mail_type_id":"1",
        "variables":{
            "email":recipient_email
        }
        
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 200:
        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Email sending failed.')

def send_follow(recipient_email):
    url = 'https://api.msg91.com/api/v5/email/send'
    headers = {
        'authkey': MSG91_AUTH_KEY,
    }
    data = {
        'sender': MSG91_SENDER_ID,
         
        'to': [
        {
            'email': recipient_email 
        }
        ],
        "from": {
             "email": "anandak@weddingvia.in"
         }, 
        "domain":"weddingvia.in",
        "template_id":"ticket_followup_final1",
        "mail_type_id":"1",
        "variables":{
            "email":recipient_email
        }
        
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 200:
        return HttpResponse('Email sent successfully!')
    else:
        return HttpResponse('Email sending failed.')


def index(request):
    return render(request, "feedback.html")

def feedback_form(request):
    name = request.POST["name"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    budget = request.POST["budget"]
    message = request.POST["message"]
    today = datetime.now() 
    
    today = datetime.now()
    Feedback.objects.create(
        name=name,
        email=email,
        phone=phone,
        category=budget,
        message=message,
       
        date_time=today,
        status="Unopened"
    )

    success_message = "Thank you for your feedback!"  # Success message to be displayed on the form page

    return render(request, 'feedback.html', {'success_message': success_message})

def follow(request, feed_id, subject, message):
    # Render the follow-up page with the subject and message
    return render(request, 'followup.html', {'feed_id': feed_id, 'subject': subject, 'message': message})


def resolve_complaint(request, feed_id):
    if request.method == 'POST':
        staff = request.POST.get('staff')
        feedback = Feedback.objects.get(feed_id=feed_id)
        feedback.staff=staff
        feedback.status = 'Accepted'
        email=feedback.email
        print(email)
        feedback.save()
        send_email(email)
        return redirect('table') 
     
def solved(request, feed_id):
    if request.method == 'POST':
        reply_text = request.POST.get('replyText', '')
        feedback = Feedback.objects.get(feed_id=feed_id)
        feedback.reply = reply_text
        feedback.status = 'Resolved'
        email=feedback.email
        print(email)
        feedback.save()
        send_complaint(email)
        return redirect('table') 

def follow(request, feed_id):
    if request.method == 'POST':
        reply_text = request.POST.get('replyText', '')
        feedback = Feedback.objects.get(feed_id=feed_id)
        feedback.reply = reply_text
        feedback.status = 'Followed'
        email=feedback.email
        #print(email)
        feedback.save()
        send_follow(email)
        return redirect('table') 

def follow_up_complaint(request, feed_id):
    feedback = Feedback.objects.get(feed_id=feed_id)
    subject = feedback.category
    message = feedback.message
    return redirect('follow', feed_id=feed_id, subject=subject, message=message)

def complaint_list(request):
    data = Feedback.objects.all()
    return render(request, "index.html", {"data": data})

from django.db.models import Q

from datetime import datetime

def table(request):
    search_query = request.GET.get('search')
    if search_query:
        data = Feedback.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(status__icontains=search_query)
        ).order_by('-feed_id')
    else:
        data = Feedback.objects.all().order_by('-feed_id')

    # Fetch the current time
    current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    return render(request, "complaint_table.html", {"data": data, "current_time": current_time})

# views.py
# complaints/views.py
from django.http import JsonResponse

def delete_followed_complaint(request):
    if request.method == 'POST':
        feed_ids = request.POST.getlist('feed_ids[]')
        print("Received feed_ids:", feed_ids)  # Add this line to check the feed_ids received in the server console
        Feedback.objects.filter(feed_id__in=feed_ids, status='Resolved').delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

from django.http import JsonResponse
from django.utils import timezone
from .models import Feedback

def delete_followed_rows(request):
    current_time = timezone.now()
    one_minute_ago = current_time - timezone.timedelta(minutes=1)
    deleted_count = Feedback.objects.filter(status="Resolved", date_time__lte=one_minute_ago).delete()[0]
    
    return JsonResponse({"message": f"{deleted_count} Resolved rows deleted successfully."})

from django.http import JsonResponse
  # Import your model

def delete_warning_rows(request):
    try:
        warning_rows = Feedback.objects.filter(status="Resolved")
        warning_rows.delete()
        return JsonResponse({"message": "Resolved rows deleted successfully."})
    except Exception as e:
        return JsonResponse({"message": f"Error deleting warning rows: {str(e)}"}, status=500)
