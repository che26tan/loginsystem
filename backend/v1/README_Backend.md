

# LoginSystem API

- The **LoginSystem API** is a secure and scalable backend built with Django and Django REST Framework for managing user authentication and identity.
- It provides essential RESTful endpoints for user signup, login, logout, JWT session handling, password reset, profile updates, and optional support for two-factor authentication (2FA) via email or phone.
- Designed to integrate seamlessly with web and mobile applications, all endpoints communicate using clean JSON and follow best practices for modern backend development.

---


## ✨ Features

- ✅ **User Registration (Signup)**  
  Register users with validation, duplicate checks, and support for phone/email-based profiles.

- 🔐 **JWT-Based Authentication**  
  Secure login and session management using access and refresh tokens.

- 🔄 **Token Refresh & Validation**  
  Easily renew access tokens without re-authentication and validate token integrity.

- 👤 **User Login / Logout**  
  Login with username and password, and securely log out with token invalidation support.

- ✏️ **Update User Profile**  
  Authenticated users can update their email, phone number, or other profile data.

- 🗑️ **Delete Account**  
  Users can permanently delete their account.

- 📩 **Email & Phone Verification**  
  OTP-based email and phone verification system with support for resend and confirmation.

- 🔁 **Password Reset Workflow**  
  Secure multi-step flow: Forgot password → OTP verification → Reset password.

- 🔑 **Password Change**  
  Authenticated users can update their password by providing the old password.

- 📱 **Country-wise Phone Support**  
  Register and verify phone numbers using country code, name, and ISO alpha codes.

- 📦 **API-Ready JSON Format**  
  All requests and responses use clean JSON for easy frontend integration.

- 📘 **Modular & Scalable**  
  Designed with extensibility in mind — easily plug in email/SMS services or external identity providers.

---

## 🧩 Planned Features

- 🛡️ **Two-Factor Authentication (2FA)**  
  Future enhancement to enable optional 2FA via email or SMS for added login security.

---
## 🧰 Technologies Used

- #### 🖥️**Backend**  
    🐍 **Python** — Core programming language for backend logic.  
    🌐 **Django** — High-level web framework for rapid development and clean design.  
    ⚙️ **Django REST Framework (DRF)** — Toolkit for building robust Web APIs.

- #### 🗄️ **Database & Caching**
    💾 **MySQL** — Relational database for persistent data storage.  
    🔄 **Redis** — Used for caching and temporary storage (e.g., OTP, token tracking).  

- #### 🔐 **Authentication**
    🔑 **JWT Authentication** — Secure, stateless authentication with access and refresh tokens.  

- #### ⚙️ **Optional / Extendable**
    🕒 **Celery** *(optional)* — Can be integrated for background tasks like sending OTPs or emails.  
    📩 **SMTP / Twilio** *(optional)* — Future integration for email or SMS-based verification and communication.  

- #### 🚢 **Deployment**
    🐳 **Docker** — Containerization for consistent environment setup.  
    🌐 **Nginx + Gunicorn** — Production-grade web server setup for serving Django applications.  
---
## ⚙️ Installation

Follow these steps to set up the project locally:

- ### Clone the Repository

    ```bash
    git clone https://github.com/che26tan/loginsystem.git
    cd loginsystem
    ```

- ### Install Python Dependencies
    It's recommended to use a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate      # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
- ### Apply Migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
- ### Run the Development Server
    ```bash
    python manage.py runserver
    ```
    Then open your browser and visit: [Go to Browser](http://127.0.0.1:8000)

---

## 📌 Usage / Examples

Replace tokens and data as needed.  
You can test these using curl, Postman, or any frontend client.

- ### 🔐 1. User Signup

    Endpoint: [POST] http://127.0.0.1:8000/auth/user/signup/
    ```bash
    Request (JSON):

    {
        "username": "jane_smith",
        "email": "jane.smith@example.com",
        "password": "StrongPass456",
        "password2": "StrongPass456",
        "country_phone_code": 1,
        "country_alpha_code": "US",
        "country_name": "United States",
        "phone_number": "1234567890",
        "gender": 2,
        "dob": "1998-12-05"
    }
    ```

- ### 🔓 2. User Login

    Endpoint: [POST] http://127.0.0.1:8000/auth/user/login/
    ```bash
    Basic Auth:

    username = "jane_smith",
    password = "StrongPass456"

    ```

- ### 🚪 3. Logout (Authenticated)

    Endpoint: [POST] http://127.0.0.1:8000/auth/user/logout/
    ```bash
    Headers:
    Authorization: Bearer <your_access_token>

    Request (JSON):
    {
        "refresh" : "<Refresh Token>"
    }
    ```

- ### 🔁 4. Get New Access Token Using Refresh Token

    Endpoint: [POST] http://127.0.0.1:8000/auth/jwt/get-access/
    ```bash
    Request (JSON):
    {
        "refresh": "<your_refresh_token>"
    }
    ```

- ### 🔁 5. Get New Refresh Token Using Refresh Token

    Endpoint: [POST] http://127.0.0.1:8000/auth/jwt/get-refresh/
    ```bash
    Request (JSON):
    {
        "refresh": "<your_refresh_token>"
    }
    ```
    
- ### 🔐 6. Change Password

    Endpoint:
    POST http://127.0.0.1:8000/auth/password/change/

    ```bash
    Headers:
    Authorization: Bearer <your_access_token>

    Request (JSON):
    {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password1": "ABC12345678", # New Password
        "password2": "ABC12345678" # Confirm Password
    }
    ```
---

## 🧑‍🔬 About Me
- # Hi, I'm Chetan Sharma! 👋

    **I am a Python Developer working in Web Development, Data Science, and Machine Learning projects. I have hands-on experience with Django, Django REST Framework, and Angular for building full-stack applications. In the field of ML and DL, I work extensively with libraries such as NumPy, Pandas, Scikit-learn, TensorFlow, and Keras to build models for classification, regression, NLP, and computer vision tasks. I am also experienced with databases like MySQL and MongoDB, and deploy applications using Docker and AWS.**


- ## 🛠 Skills

    - 👨‍💻 **Programming Languages**  
        Python, C, C++, OOPs, HTML, CSS, SQL, JavaScript

    - 🧰 **Frameworks & Libraries**  
        Django, Django Rest Framework (DRF), Angular 19, Celery, NumPy, Pandas, Seaborn, Matplotlib, Openpyxl, BeautifulSoup, Selenium, Scikit-learn

    - 🤖 **Machine Learning & Deep Learning**  
        Scikit-learn, TensorFlow, Keras, CNN, RNN, LSTM, NLP, Unsupervised Learning

    - 🗄️ **Databases**  
        MySQL, SQLite, MongoDB, Redis

    - 📊 **Analytics & Tools**  
        Tableau, Excel

    - 🐳 **DevOps & Deployment**  
        Docker, AWS


- ## 🔗 Links
    - [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sharma26chetan)
    - [![GitHub](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/che26tan/)

---

## 📄 License

- his project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).  
- You are free to use, modify, and distribute this software with proper attribution.

---
## 👨‍💻 Author

- [@Chetan Sharma](https://www.github.com/che26tan) — Developer & Maintainer


## 💬 Feedback

- If you have any feedback, please reach out to us at [Gmail](sharma26chetan@gmail.com)


## 📖 Documentation


- For a quick demo of key endpoints and usage examples, visit the [Usage / Examples](#-usage--examples) section above.

- For comprehensive setup instructions, environment configuration, and complete API references, please refer to the [Project Documentation](https://github.com/che26tan/loginsystem/blob/main/documentation.md). 

