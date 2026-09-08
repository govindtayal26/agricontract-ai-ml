from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from marketplace import views


urlpatterns = [

    # Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Home
    path(
        '',
        views.home,
        name='home'
    ),

    # Farmer - Add Crop
    path(
        'add-crop/',
        views.add_crop,
        name='add_crop'
    ),

    # Buyer - Send Offer
    path(
    'send-offer/<int:crop_id>/',
    views.send_offer,
    name='send_offer'
),

    # Farmer - Accept / Reject Offer
    path(
        'update-contract/<int:contract_id>/',
        views.update_contract,
        name='update_contract'
    ),
    path(
    "crop-price-predictor/",
    views.crop_price_predictor,
    name="crop_price_predictor"
),
    # Buyer Dashboard
    path(
        'buyer-dashboard/',
        views.buyer_dashboard,
        name='buyer_dashboard'
    ),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='index.html'
        ),
        name='login'
    ),

    # Logout
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Farmer Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # Registration
    path(
        'register/',
        views.register_user,
        name='register'
    ),

    # Weather API
    path(
        'api/weather/',
        views.weather_api_view,
        name='weather_api'
    ),

    # Disease Detection
    path(
        'disease-detector/',
        views.disease_detector,
        name='disease_detector'
    ),

    # Contract Chat
    path(
        'chat/<int:contract_id>/',
        views.chat_view,
        name='chat'
    ),

    # AI Chatbot
    path(
        'ai-chatbot/',
        views.ai_chatbot,
        name='ai_chatbot'
    ),
]

path('logout/', views.logout_user, name='logout'),



# Media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )