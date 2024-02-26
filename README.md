# ADS_Mini_Project: Samsung Mobile Phones review
## Description
This Project is mainly combine of two parts. 
- Data scraping which will scrape mobile phone reviews from https://www.gsmarena.com/
- Django project that will perform sentiment analysis and display the figure base on user selected models

---
## Project Setup
1. Create virtual environment using venv or anaconda and activate it.
2. install requirements.txt by executing this command  
    ```pip install -r requirements.txt```
3. cd to the directory that contains manage.py and execute these command for database setup
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Start the Django application
    ```
    python manage.py runserver
    ```
5. Go to your web browser and enter this URL - **http://127.0.0.1:8000/** or you can get the url from the terminal like screenshot below:
![hints](ReadMe_hints.png)
 

---


## Screenshots
### Login Page
![Login Page](ads_login.png)

### User Registration Page
![User Registration Page](ads_register.png)

### User Registration Page - Username taken
![User Registration Page - Username taken](ads_register_username_taken.png)

### User Registration Page - Invalid Password
![User Registration Page - Invalid Password](ads_register_password_not_same.png)

### User Registration Page - Valid Password 
![User Registration Page - Valid Password ](ads_register_password_valid.png)

### User Registration Page - Registration succeeded
![User Registration Page - Registration succeeded](ads_register_success.png)

### Dashboard
![Dashboard](ads_dashboard.png)

### Dashboard - Models selection
![Dashboard - Models selection](ads_dashboard_model_selection.png)

### Dashboard - Figures
![Dashboard - Figures](ads_dashboard_figure_1.png)

### Dashboard - Figures cont
![Dashboard - Figures(cont)](ads_dashboard_figure_2.png)