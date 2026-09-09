
import os
import numpy as np

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages

from .models import Crop, Contract, Message
from .forms import CropForm
from .services import get_farmer_weather
from .ml_predictor import predict_crop_price
from .plant_disease_service import predict_disease


# ============================================================
# AI MODEL CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# The model is NOT loaded when Django starts.
# It is loaded only when the disease detector is actually used.

model = None

classes = [
    "Early Blight",
    "Late Blight",
    "Healthy"
]


def get_model():
    """
    Lazy-load the TensorFlow disease detection model.

    This prevents Django from crashing when the model file
    does not exist during commands such as:

        python manage.py check
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver
    """

    global model

    if model is None:

        model_path = os.path.join(
            BASE_DIR,
            "model",
            "potato_model.h5"
        )

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"Model not found: {model_path}. "
                f"Train the disease detection model first."
            )

        model = load_model(model_path)

    return model


# ============================================================
# HOME
# ============================================================

def home(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    if search_query:

        crops = Crop.objects.filter(
            name__icontains=search_query
        ).order_by(
            "-created_at"
        )

    else:

        crops = Crop.objects.all().order_by(
            "-created_at"
        )

    return render(
        request,
        "index.html",
        {
            "crops": crops
        }
    )

@login_required
def crop_price_predictor(request):

    prediction = None
    error = None

    if request.method == "POST":

        try:
            crop = request.POST.get("crop", "").strip()
            state = request.POST.get("state", "").strip()

            month = int(request.POST.get("month"))
            rainfall = float(request.POST.get("rainfall"))
            temperature = float(request.POST.get("temperature"))
            quantity = float(request.POST.get("quantity"))
            previous_price = float(
                request.POST.get("previous_price")
            )

            if not crop or not state:
                raise ValueError(
                    "Crop and state are required."
                )

            if not 1 <= month <= 12:
                raise ValueError(
                    "Month must be between 1 and 12."
                )

            if quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero."
                )

            if previous_price <= 0:
                raise ValueError(
                    "Previous price must be greater than zero."
                )

            prediction = predict_crop_price(
                crop=crop,
                state=state,
                month=month,
                rainfall=rainfall,
                temperature=temperature,
                quantity=quantity,
                previous_price=previous_price
            )

        except (ValueError, TypeError) as e:
            error = str(e)

        except FileNotFoundError as e:
            error = str(e)

    return render(
        request,
        "crop_price_predictor.html",
        {
            "prediction": prediction,
            "error": error,
        }
    )
# ============================================================
# SEND OFFER
# ============================================================

@login_required
def send_offer(request, crop_id):

    # Only POST requests are allowed
    if request.method != "POST":
        return redirect("home")

    # Get the crop
    crop = get_object_or_404(
        Crop,
        id=crop_id
    )

    # Only buyers can send offers
    if not hasattr(request.user, "userprofile") or request.user.userprofile.role != "buyer":
        messages.error(
            request,
            "Only buyers can send offers."
        )
        return redirect("home")

    # Farmer cannot send offer on their own crop
    if crop.farmer == request.user:
        messages.error(
            request,
            "You cannot send an offer to your own crop."
        )
        return redirect("home")

    # Get price from form
    price = request.POST.get("price", "").strip()

    # Check empty price
    if not price:
        messages.error(
            request,
            "Please enter an offer price."
        )
        return redirect("home")

    # Validate price
    try:
        price = float(price)

        if price <= 0:
            raise ValueError

    except ValueError:
        messages.error(
            request,
            "Please enter a valid offer price greater than zero."
        )
        return redirect("home")

    # Create contract / offer
    Contract.objects.create(
        farmer=crop.farmer,
        buyer=request.user,
        crop=crop,
        offered_price=price,
        status="pending"
    )

    # Success message
    messages.success(
        request,
        "Offer sent successfully!"
    )

    return redirect("home")


# ============================================================
# ADD CROP
# ============================================================

@login_required
def add_crop(request):

    if request.method == "POST":

        form = CropForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            crop = form.save(
                commit=False
            )

            crop.farmer = request.user

            crop.save()

            messages.success(
                request,
                "Crop added successfully!"
            )

            return redirect("home")

    else:

        form = CropForm()

    return render(
        request,
        "add_crop.html",
        {
            "form": form
        }
    )


# ============================================================
# AI DISEASE DETECTOR
# ============================================================

# ============================================================
# AI POTATO DISEASE DETECTOR
# ============================================================
def disease_detector(request):
    """
    Handle potato leaf image upload and disease prediction.

    Returns:
        GET  -> Disease detector page
        POST -> JSON prediction result
    """

    if request.method != "POST":
        return render(request, "disease_detector.html")

    uploaded_file = request.FILES.get("crop_image")

    # -------------------------------------------------
    # 1. Validate uploaded image
    # -------------------------------------------------

    if not uploaded_file:
        return JsonResponse(
            {
                "error": "Please upload a potato leaf image."
            },
            status=400
        )

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if uploaded_file.content_type not in allowed_types:
        return JsonResponse(
            {
                "error": (
                    "Invalid image format. "
                    "Please upload JPG, PNG, or WEBP."
                )
            },
            status=400
        )

    # Maximum file size: 5 MB
    max_file_size = 5 * 1024 * 1024

    if uploaded_file.size > max_file_size:
        return JsonResponse(
            {
                "error": (
                    "Image is too large. "
                    "Maximum allowed size is 5 MB."
                )
            },
            status=400
        )

    file_path = None

    try:
        # -------------------------------------------------
        # 2. Temporarily save uploaded image
        # -------------------------------------------------

        storage = FileSystemStorage()

        filename = storage.save(
            uploaded_file.name,
            uploaded_file
        )

        file_path = storage.path(filename)

        # -------------------------------------------------
        # 3. Run AI prediction
        # -------------------------------------------------

        prediction = predict_disease(file_path)

        disease = prediction["disease"]
        confidence = float(prediction["confidence"])

        # -------------------------------------------------
        # 4. Generate disease-specific recommendation
        # -------------------------------------------------

        disease_info = {
            "Early_blight": {
                "status": "Warning",
                "advice": (
                    "Early Blight detected. Remove infected "
                    "leaves and maintain good airflow around "
                    "the plants. Avoid prolonged leaf moisture "
                    "and monitor the crop regularly."
                )
            },

            "Late_blight": {
                "status": "Danger",
                "advice": (
                    "Late Blight detected. Remove severely "
                    "infected plant material and isolate "
                    "affected plants where possible. "
                    "Consult an agricultural expert for "
                    "appropriate disease-management treatment."
                )
            },

            "Healthy": {
                "status": "Healthy",
                "advice": (
                    "The potato leaf appears healthy. "
                    "Continue regular crop monitoring, "
                    "maintain proper irrigation and nutrition, "
                    "and watch for new symptoms."
                )
            }
        }

        # -------------------------------------------------
        # 5. Get information for predicted disease
        # -------------------------------------------------

        result_info = disease_info.get(
            disease,
            {
                "status": "Unknown",
                "advice": (
                    "The model could not confidently "
                    "identify this condition. Please upload "
                    "a clear potato leaf image."
                )
            }
        )

        # -------------------------------------------------
        # 6. Confidence threshold
        # -------------------------------------------------

        confidence_threshold = 60.0

        if confidence < confidence_threshold:
            status = "Low Confidence"

            advice = (
                "The AI is not sufficiently confident "
                "about this prediction. Please upload a "
                "clearer potato leaf image with the leaf "
                "visible and well focused."
            )

        else:
            status = result_info["status"]
            advice = result_info["advice"]

        # -------------------------------------------------
        # 7. Return prediction to frontend
        # -------------------------------------------------

        return JsonResponse(
            {
                "success": True,
                "disease": disease,
                "confidence": f"{confidence:.2f}%",
                "status": status,
                "advice": advice
            }
        )

    except FileNotFoundError:
        return JsonResponse(
            {
                "error": (
                    "AI model file was not found. "
                    "Please check the trained model."
                )
            },
            status=500
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        return JsonResponse(
            {
                "error": (
                    "Unable to analyze the image right now. "
                    "Please try again."
                ),
                "details": str(e)
            },
            status=500
        )

    finally:
        # -------------------------------------------------
        # 8. Always remove temporary uploaded image
        # -------------------------------------------------

        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
      


        # ----------------------------------------------------
        # AGRICULTURAL ADVICE
        
# ============================================================
# FARMER / BUYER DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    role = request.user.userprofile.role

    # Buyer
    if role == "buyer":

        return redirect(
            "buyer_dashboard"
        )

    # Farmer crops
    my_crops = Crop.objects.filter(
        farmer=request.user
    )

    # Farmer contracts
    contracts = Contract.objects.filter(
        farmer=request.user
    )

    return render(
        request,
        "dashboard.html",
        {
            "my_crops": my_crops,
            "contracts": contracts
        }
    )


# ============================================================
# REGISTER USER
# ============================================================

def register_user(request):

    if request.method != "POST":

        return redirect("home")

    # --------------------------------------------------------
    # Get form values
    # --------------------------------------------------------

    full_name = request.POST.get(
        "name",
        ""
    ).strip()

    username = request.POST.get(
        "username",
        ""
    ).strip()

    password = request.POST.get(
        "password",
        ""
    )

    confirm_password = request.POST.get(
        "confirm_password",
        ""
    )

    role = request.POST.get(
        "role",
        ""
    ).strip().lower()

    # --------------------------------------------------------
    # Validate name
    # --------------------------------------------------------

    if not full_name:

        messages.error(
            request,
            "Please enter your name."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Validate email / username
    # --------------------------------------------------------

    if not username:

        messages.error(
            request,
            "Please enter your email."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Check existing user
    # --------------------------------------------------------

    if User.objects.filter(
        username=username
    ).exists():

        messages.error(
            request,
            "This email is already registered."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Validate password
    # --------------------------------------------------------

    if len(password) < 8:

        messages.error(
            request,
            "Password must contain at least 8 characters."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Confirm password
    # --------------------------------------------------------

    if password != confirm_password:

        messages.error(
            request,
            "Passwords do not match."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Validate role
    # --------------------------------------------------------

    if role not in [
        "farmer",
        "buyer"
    ]:

        messages.error(
            request,
            "Please select Farmer or Buyer."
        )

        return redirect("home")

    # --------------------------------------------------------
    # Create Django user
    # --------------------------------------------------------

    user = User.objects.create_user(
        username=username,
        email=username,
        password=password
    )

    # --------------------------------------------------------
    # Save full name
    # --------------------------------------------------------

    user.first_name = full_name

    user.save()

    # --------------------------------------------------------
    # Update UserProfile
    # --------------------------------------------------------

    profile = user.userprofile

    profile.role = role

    profile.save()

    # --------------------------------------------------------
    # Login user automatically
    # --------------------------------------------------------

    login(
        request,
        user
    )

    messages.success(
        request,
        f"Welcome {full_name}!"
    )

    return redirect(
        "home"
    )


# ============================================================
# LOGOUT USER
# ============================================================

def logout_user(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")


# ============================================================
# WEATHER API
# ============================================================

def weather_api_view(request):

    lat = request.GET.get(
        "lat"
    )

    lon = request.GET.get(
        "lon"
    )

    if lat and lon:

        data = get_farmer_weather(
            lat,
            lon
        )

        return JsonResponse(
            data
        )

    return JsonResponse(
        {
            "error": "No coordinates provided"
        },
        status=400
    )


# ============================================================
# UPDATE CONTRACT
# ============================================================

@login_required
def update_contract(request, contract_id):

    # Make sure the user has a profile
    if not hasattr(request.user, "userprofile"):
        return redirect("home")

    # Only farmers can accept/reject offers
    if request.user.userprofile.role != "farmer":
        return redirect("buyer_dashboard")

    # Get only contracts belonging to this farmer
    contract = get_object_or_404(
        Contract,
        id=contract_id,
        farmer=request.user
    )

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "accept":

            contract.status = "accepted"
            contract.save()

        elif action == "reject":

            contract.status = "rejected"
            contract.save()

    return redirect("dashboard")

# ============================================================
# BUYER DASHBOARD
# ============================================================

@login_required
def buyer_dashboard(request):

    contracts = Contract.objects.filter(
        buyer=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "buyer_dashboard.html",
        {
            "contracts": contracts
        }
    )


# ============================================================
# CONTRACT CHAT
# ============================================================

@login_required
def chat_view(
    request,
    contract_id
):

    contract = get_object_or_404(
        Contract,
        id=contract_id
    )

    # Only the farmer and buyer involved in
    # this contract can access the chat.

    if (
        request.user != contract.buyer
        and request.user != contract.farmer
    ):

        return redirect(
            "dashboard"
        )

    messages_list = Message.objects.filter(
        contract=contract
    ).order_by(
        "created_at"
    )

    if request.method == "POST":

        text = request.POST.get(
            "text",
            ""
        ).strip()

        if text:

            Message.objects.create(
                contract=contract,
                sender=request.user,
                text=text
            )

        return redirect(
            "chat",
            contract_id=contract.id
        )

    return render(
        request,
        "chat.html",
        {
            "contract": contract,
            "messages": messages_list
        }
    )


# ============================================================
# AI AGRICULTURAL CHATBOT
# ============================================================

def ai_chatbot(request):

    if request.method == "POST":

        msg = request.POST.get(
            "message",
            ""
        ).strip().lower()

        # ----------------------------------------------------
        # PROJECT
        # ----------------------------------------------------

        if (
            "project" in msg
            or "explain" in msg
        ):

            reply = """
This project is an integrated agricultural
platform combining an assured marketing system
with AI-based crop disease detection.

It helps farmers in two major areas:

1. Crop health monitoring
2. Guaranteed market access

Farmers can connect directly with buyers,
manage crops and contracts, and use AI to
detect diseases in plant leaves.
"""

        # ----------------------------------------------------
        # PROBLEM
        # ----------------------------------------------------

        elif "problem" in msg:

            reply = """
Farmers face problems such as unstable market
prices, middlemen exploitation, delayed payments,
and crop losses caused by diseases.

AgriContract addresses these problems by providing
a digital marketplace for direct farmer-buyer
connections and AI-based early disease detection.
"""

        # ----------------------------------------------------
        # ALGORITHM / CNN
        # ----------------------------------------------------

        elif (
            "algorithm" in msg
            or "cnn" in msg
        ):

            reply = """
The disease detection system uses a Convolutional
Neural Network (CNN), a deep learning algorithm
for image classification.

CNNs automatically learn visual features such as
edges, textures, shapes, and disease patterns from
plant leaf images.

The model classifies potato leaves into:

• Healthy
• Early Blight
• Late Blight
"""

        # ----------------------------------------------------
        # DATASET
        # ----------------------------------------------------

        elif "dataset" in msg:

            reply = """
The disease detection system uses the PlantVillage
dataset.

For the potato disease detection task, the relevant
classes include:

• Healthy
• Early Blight
• Late Blight

Images are resized and normalized before being
provided to the neural network.
"""

        # ----------------------------------------------------
        # PREPROCESSING
        # ----------------------------------------------------

        elif "preprocessing" in msg:

            reply = """
Image preprocessing includes:

• Resizing images to 224x224 pixels
• Converting images into numerical arrays
• Normalizing pixel values
• Data augmentation during model training

Data augmentation can include rotation, flipping,
zooming, and other transformations to improve
generalization.
"""

        # ----------------------------------------------------
        # TRAINING
        # ----------------------------------------------------

        elif "training" in msg:

            reply = """
The disease detection model is trained using
supervised learning.

The labeled dataset is divided into training,
validation, and testing data.

During training, the CNN learns visual patterns
associated with different potato leaf diseases.

The final layer uses softmax classification to
produce probabilities for each disease class.
"""

        # ----------------------------------------------------
        # ACCURACY / RESULTS
        # ----------------------------------------------------

        elif (
            "accuracy" in msg
            or "result" in msg
        ):

            reply = """
Model accuracy should be reported from the actual
evaluation results of the trained model.

Important evaluation metrics include:

• Accuracy
• Precision
• Recall
• F1-score
• Confusion matrix

We should not claim a specific accuracy until the
trained model has actually been evaluated on a
held-out test dataset.
"""

        # ----------------------------------------------------
        # EARLY BLIGHT
        # ----------------------------------------------------

        elif "early blight" in msg:

            reply = """
Early Blight is a fungal disease that can produce
brown or dark lesions on potato leaves.

Disease management should be based on actual field
conditions and local agricultural guidance.
"""

        # ----------------------------------------------------
        # LATE BLIGHT
        # ----------------------------------------------------

        elif "late blight" in msg:

            reply = """
Late Blight is a serious potato disease that can
spread rapidly under favorable environmental
conditions, particularly cool and humid conditions.

Farmers should monitor crops regularly and follow
local agricultural disease-management guidance.
"""

        # ----------------------------------------------------
        # PLATFORM / MARKETING
        # ----------------------------------------------------

        elif (
            "platform" in msg
            or "marketing" in msg
        ):

            reply = """
The assured marketing platform connects farmers
directly with buyers.

Farmers can list their crops, while buyers can
browse available crops and submit offers.

The contract system allows both parties to manage
accepted and rejected offers digitally.
"""

        # ----------------------------------------------------
        # IMPACT
        # ----------------------------------------------------

        elif "impact" in msg:

            reply = """
The system combines agricultural commerce with
AI-based crop monitoring.

Potential benefits include:

• Earlier disease detection
• Better crop monitoring
• Direct farmer-buyer communication
• Digital contract management
• Better access to market information
"""

        # ----------------------------------------------------
        # FUTURE
        # ----------------------------------------------------

        elif "future" in msg:

            reply = """
Future improvements can include:

• More crop disease classes
• Transfer learning
• Grad-CAM explainability
• Crop recommendation
• Disease-risk prediction
• Market price prediction
• Weather-based recommendations
• IoT sensor integration
• Mobile application
• RAG-based agricultural assistant
"""

        # ----------------------------------------------------
        # METHODOLOGY
        # ----------------------------------------------------

        elif "methodology" in msg:

            reply = """
The methodology consists of several stages:

1. Data collection
2. Image preprocessing
3. Data augmentation
4. Deep learning model training
5. Model evaluation
6. Django integration
7. Disease prediction
8. Agricultural marketplace
9. Contract management
10. AI-based agricultural intelligence

The goal is to combine machine learning,
deep learning, and a real-world web application.
"""

        # ----------------------------------------------------
        # DEFAULT RESPONSE
        # ----------------------------------------------------

        else:

            reply = """
I am Smart Agri Jarvis 🤖

I can explain:

• AgriContract project
• CNN
• Deep learning
• Dataset
• Image preprocessing
• Model training
• Model evaluation
• Potato diseases
• Contract farming
• Marketplace
• Future improvements

Try asking:

"Explain project"

"What algorithm do you use?"

"What is CNN?"

"Explain the dataset"

"How does disease detection work?"

"What is contract farming?"
"""

        return JsonResponse(
            {
                "reply": reply
            }
        )

    return render(
        request,
        "chatbot.html"
    )

