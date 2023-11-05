from django.urls import path
from .import views 
from . views import send_email
urlpatterns = [
     path("",views.index,name="index"),
     path("index",views.index,name="index"),
     path("feedback_form",views.feedback_form,name="feedback_form"),
     path("complaint_list",views.complaint_list,name="complaint_list"),
     path('send_email',views.send_email, name='send_email'),
     path('resolve_complaint/<int:feed_id>/', views.resolve_complaint, name='resolve_complaint'),
     path('follow_up_complaint/<int:feed_id>/', views.follow_up_complaint, name='follow_up_complaint'),
     path("follow",views.follow,name="follow"),
     path("send_complaint",views.send_complaint,name="send_complaint"),
     path("solved/<int:feed_id>/",views.solved,name="solved"),
     path("follow/<int:feed_id>/",views.follow,name="follow"),
     path("table",views.table,name="table"),
     path('delete_followed_complaint/', views.delete_followed_complaint, name='delete_followed_complaint'),
     path('delete_followed_rows/', views.delete_followed_rows, name='delete_followed_rows'),
     path('delete_warning_rows/', views.delete_warning_rows, name='delete_warning_rows'),
     path("login",views.login,name="login"),
     path("login_form",views.login_form,name="login_form"),
     
     
    
]