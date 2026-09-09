# 🌾 AgriContract

### AI-Powered Agriculture Marketplace & Smart Farming Platform

AgriContract is a full-stack agriculture platform built with **Django, Machine Learning, and Deep Learning**.

It connects farmers and buyers while providing AI-powered agricultural assistance, weather information, and **potato leaf disease detection using MobileNetV2 transfer learning**.

---

## 🌐 Live Demo

🔗 https://agricontract-2hba.onrender.com

---

## ✨ Features

- 👨‍🌾 Farmer & Buyer authentication
- 🛒 Agriculture marketplace
- 📦 Farmer product/listing management
- 🤝 Buyer offers
- 💬 Farmer–Buyer interaction
- 🌦️ Weather information
- 🤖 AI-powered potato disease detection
- 📊 Disease confidence prediction
- 🌱 Agricultural disease advice
- 🗄️ PostgreSQL production support
- ☁️ Render deployment

---

## 🤖 AI Disease Detection

AgriContract includes a Deep Learning model that detects potato leaf diseases from uploaded images.

### Supported Diseases

| Class | Description |
|---|---|
| 🟢 Healthy | Healthy potato leaf |
| 🟠 Early Blight | Early blight detected |
| 🔴 Late Blight | Late blight detected |

### AI Pipeline

```text
Potato Leaf Image
        ↓
Image Validation
        ↓
Resize → 224 × 224
        ↓
Preprocessing
        ↓
MobileNetV2
        ↓
Global Average Pooling
        ↓
Dense Layer
        ↓
Dropout
        ↓
Softmax
        ↓
Disease + Confidence
        ↓
Agricultural Advice
