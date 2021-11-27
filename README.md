# Pinocchio

Pinocchio is a website for students to register for their college courses. The process is simple. The college admin will create all the courses and then create the registration form. The registration starts on a particular date and time and stays live till the registration end time. The student and faculties need to signup on the website, then college admin adds courses and creates registration for the students. The students can register and unregister for the courses for as long as the registration is live, after that no changes will be allowed. Also a student can register for courses which are offered in his/her next semester.

## Software Requirements

* Python `3.10`
* Git

## How to get started

### Downloading the Code

* Go to (<https://github.com/shreygoel7/Pinocchio>) and click on **Fork**
* You will be redirected to *your* fork, `https://github.com/<your_user_name>/Pinocchio`
* Open the terminal, change to the directory where you want to clone the **Pinocchio** repository
* Clone your repository using `git clone https://github.com/<your_user_name>/Pinocchio`
* Enter the cloned directory using `cd Pinocchio/`

### Setting up virtual environment (Optional)

You can do this using any method. Below is a method that I find very easy to use in **Windows**
* Install `virtualenvwrapper-win`  
  * on **Windows CMD**: `pip install virtualenvwrapper-win`
* Create new virtual env
  * on **Windows CMD**: `mkvirtualenv <your_env_name>` E.g. `mkvirtualenv pinocchio`

**Info:** You can activate your virtual environment using `workon <your_env_name>` and deactivate it using `deactivate <your_env_name>`

### Installing Dependencies

* Change directory to **Pinocchio** `cd Pinocchio`
* Install the requirements: `pip install -r requirements.txt`

### Running server

* Run the server `python manage.py runserver`


### Running tests

* Run the server `python manage.py test`
* For checking coverage run `coverage run python manage.py test` and then run `coverage report`
* For testing purpose, please see the `credentials.txt` file for some sample credentials.
