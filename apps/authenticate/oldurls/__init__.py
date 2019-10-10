from django.urls import include, path, re_path
from mighty.apps.authenticate import views

urlpatterns = [
    path('email/', include([
        path('create/', views.email.EmailCreate.as_view(), name='email-create'),
        path('<uuid:uid>/', include([
            path('update/<str:display>/', views.email.EmailUpdate.as_view(), name='email-update'),
            path('delete/<str:display>/', views.email.EmailDelete.as_view(), name='email-delete'),
            path('disable/<str:display>/', views.email.EmailDisable.as_view(), name='email-disable'),
            path('enable/<str:display>/', views.email.EmailEnable.as_view(), name='email-enable'),
            path('check/<str:display>/', views.email.EmailCheckStatus.as_view(), name='email-check-status'),
            path('<str:display>/', views.email.EmailDetail.as_view(), name='email-detail'),
        ])),
        path('', views.email.EmailList.as_view(), name='email-list'),
    ])),
    path('sms/', include([
        path('create/', views.sms.SmsCreate.as_view(), name='sms-create'),
        path('<uuid:uid>/', include([
            path('update/<str:display>/', views.sms.SmsUpdate.as_view(), name='sms-update'),
            path('delete/<str:display>/', views.sms.SmsDelete.as_view(), name='sms-delete'),
            path('disable/<str:display>/', views.sms.SmsDisable.as_view(), name='sms-disable'),
            path('enable/<str:display>/', views.sms.SmsEnable.as_view(), name='sms-enable'),
            path('check/<str:display>/', views.sms.SmsCheckStatus.as_view(), name='sms-check-status'),
            path('<str:display>/', views.sms.SmsDetail.as_view(), name='sms-detail'),
        ])),
        path('', views.sms.SmsList.as_view(), name='sms-list'),
    ])),
    path('login/', include([
        path('sms/<uuid:uid>/', views.sms.LoginSms.as_view(), name='login-sms'),
        path('email/<uuid:uid>/', views.email.LoginEmail.as_view(), name='login-email'),
        path('', views.Login.as_view(), name='login'),
    ])),
]