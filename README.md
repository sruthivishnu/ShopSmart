# 🛍️ ShopSmart

An AI-powered E-Commerce Recommendation System built using **Flask**, **Machine Learning**, and **MySQL**.

ShopSmart provides intelligent product recommendations using a hybrid recommendation engine that combines content-based filtering, collaborative filtering, Apriori-based Frequently Bought Together recommendations, and personalized user recommendations.

---

# ✨ Features

- Personalized product recommendations
- Similar Products recommendation engine
- Frequently Bought Together recommendations
- Trending & Hot Picks
- Category-based shopping
- Smart product search
- Search autocomplete
- Shopping Cart
- Order Management
- User Authentication
- Product Reviews & Ratings
- Gemini AI Chatbot
- Responsive user interface

---

# 🧠 Recommendation Engine

The recommendation system combines multiple techniques:

- Content-Based Filtering (TF-IDF + Cosine Similarity)
- Collaborative Filtering
- Apriori Association Rules
- Personalized Recommendations
- Recently Viewed Products
- Hybrid Ranking Engine

---

# 🛠️ Technology Stack

## Backend

- Python
- Flask
- MySQL

## Machine Learning

- Pandas
- NumPy
- Scikit-Learn
- MLxtend

## Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates

---

# 📂 Project Structure

```
ShopSmart/
│
├── recommendation/
│   ├── hybrid.py
│   ├── content.py
│   ├── collaborative.py
│   ├── apriori.py
│   ├── frequently_bought.py
│   ├── user_recommendation.py
│   └── ...
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│
├── app.py
├── requirements.txt
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

# 📊 Dataset

The project uses product and transaction datasets to generate recommendations.

Main datasets include:

- products_cleaned.csv
- transactions.csv
- users.csv
- transactions_apriori.csv

---

# 🔒 Environment Variables

Create a `.env` file containing:

```
MYSQL_HOST=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_DB=
SECRET_KEY=
GEMINI_API_KEY=
```

---

# 📈 Future Improvements

- Product recommendation analytics
- User preference learning
- Wishlist functionality
- Payment gateway integration
- Admin dashboard
- Email notifications
- Cloud deployment

---

# 👩‍💻 Developed By

**Sruthi Sukumaran P**

Btech Graduate | Data Science Enthusiast

---

⭐ If you like this project, consider giving it a star!