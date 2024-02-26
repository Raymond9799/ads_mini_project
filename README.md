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
5. Go to your web browser and enter the URL. The URL you can get it from your terminal
    ![hints](read_me_images/ReadMe_hints.jpg)
 

---


## Screenshots
### Login Page
![Login Page](read_me_images/ads_login.jpg)

### User Registration Page
![User Registration Page](read_me_images/ads_register.jpg)

### User Registration Page - Username taken
![User Registration Page - Username taken](read_me_images/ads_register_username_taken.jpg)

### User Registration Page - Invalid Password
![User Registration Page - Invalid Password](read_me_images/ads_register_password_not_same.jpg)

### User Registration Page - Valid Password 
![User Registration Page - Valid Password ](read_me_images/ads_register_password_valid.jpg)

### User Registration Page - Registration succeeded
![User Registration Page - Registration succeeded](read_me_images/ads_register_success.jpg)

### Dashboard
![Dashboard](read_me_images/ads_dashboard.jpg)

### Dashboard - Models selection
![Dashboard - Models selection](read_me_images/ads_dashboard_model_selection.jpg)

### Dashboard - Figures
![Dashboard - Figures](read_me_images/ads_dashboard_figure_1.jpg)

### Dashboard - Figures cont
![Dashboard - Figures(cont)](read_me_images/ads_dashboard_figure_2.jpg)