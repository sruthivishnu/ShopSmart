# 🛍️ ShopSmart

> **AI-Powered E-Commerce Recommendation System built with Flask, Machine Learning, and MySQL**

ShopSmart is a full-stack e-commerce web application that provides intelligent product recommendations using a **Hybrid Recommendation Engine**. It combines **Content-Based Filtering**, **Collaborative Filtering**, and **Apriori Association Rules** to deliver personalized shopping experiences.

The application also includes smart search, category browsing, shopping cart, order management, product reviews, and an AI-powered chatbot, making it a complete end-to-end shopping platform.

---

# 📸 Application Preview

## 🏠 Homepage

![Homepage](static/screenshots/homepage.png)

---

## 📦 Product Recommendation

Features displayed:

- Product Details
- Similar Products
- Frequently Bought Together
- Trending Products
- Customer Reviews

![Product Page](static/screenshots/product-page.png)

---

## 🛍️ Category Collections

Browse premium collections with dedicated category pages.

![Category Page](static/screenshots/category-page.png)

---

## 🔍 Smart Search

Fast product search with category-aware filtering.

![Search Page](static/screenshots/search-page.png)

---

# ✨ Key Features

- 🤖 Hybrid Recommendation Engine
- 🧠 Content-Based Recommendations (TF-IDF + Cosine Similarity)
- 👥 Collaborative Filtering
- 🛒 Frequently Bought Together (Apriori Algorithm)
- ❤️ Personalized Recommendations
- 🔍 Smart Product Search
- ⚡ Search Autocomplete
- 🛍️ Shopping Cart
- 📦 Order Management
- ⭐ Product Reviews & Ratings
- 🤖 Gemini AI Chatbot
- 📱 Responsive User Interface
- 🔐 User Authentication
- 🗂️ Category-Based Shopping

---

# 🧠 Recommendation Engine Architecture

```
                        User

                          │

                          ▼

                  Product Selected

                          │

          ┌───────────────┼───────────────┐

          ▼               ▼               ▼

   Content-Based    Collaborative      Apriori

     Filtering        Filtering         FBT

          └───────────────┼───────────────┘

                          ▼

                Hybrid Ranking Engine

                          ▼

             Personalized Recommendations
```

---

# 🛠️ Technology Stack

### Backend

- Python
- Flask
- MySQL

### Machine Learning

- Pandas
- NumPy
- Scikit-Learn
- MLxtend

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2

### Tools

- Git
- GitHub
- PyCharm

---

# 📂 Project Structure

```
ShopSmart
│
├── recommendation/
│   ├── hybrid.py
│   ├── collaborative.py
│   ├── content.py
│   ├── apriori.py
│   ├── frequently_bought.py
│   ├── user_recommendation.py
│   ├── chatbot.py
│   └── ...
│
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── screenshots/
│
├── templates/
│
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/sruthivishnu/ShopSmart.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

---

# 🔒 Environment Variables

Create a `.env` file.

```
MYSQL_HOST=

MYSQL_USER=

MYSQL_PASSWORD=

MYSQL_DB=

SECRET_KEY=

GEMINI_API_KEY=
```

---

# 📊 Project Highlights

- Nearly **20,000 products**
- Hybrid Recommendation Engine
- Personalized Shopping Experience
- Category-aware Recommendations
- Smart Search & Autocomplete
- Product Reviews
- Shopping Cart
- Order Management
- Responsive UI

---

# 🚀 Future Improvements

- Admin Dashboard
- Recommendation Analytics
- Wishlist
- Payment Gateway Integration
- Email Notifications
- Docker Support
- Unit Testing
- CI/CD Pipeline

---

# 👩‍💻 Developer

**Sruthi Sukumaran P**

Btech Graduate | Aspiring Data Scientist | Python & Machine Learning Enthusiast

GitHub:
https://github.com/sruthivishnu

---

⭐ If you found this project interesting, consider giving it a star!