# Emergency-Department
 This is a simple hospital management system software focused mainly on Emergency department using MySQL Database Service.


## Table of Contents

* [About the Project](#about-the-project)
* [Toolbox](#toolbox)
* [Setting Up the Environment](#setting-up-the-environment)
* [Working Demo of the System](#working-demo-of-the-system)
* [First Entry Information](#first-entry-information)
* [Our Team](#our-team)
* [About](#about)

## About The Project
This is a simple hospital management system software focused mainly on Emergency department.

## Toolbox

- HTML
- CSS
- JavaScript
- JQuery
- Bootstrap
- Flask
    * Flask SQLAlchemy
    * Flask Blueprint
    * Flask User
    * Flask LoginManger

## Setting Up the Environment
1. Clone the repo
    - HTTPS
        ```sh
        git clone https://github.com/MostafaAbbas-git/Emergency-Department.git
        ```

1. Create a Virtual Environment (Optional)
    ```sh
    python -m venv .HIS-EMG
    ```
2. Activate the virtual environment 
    - using CMD
        ```sh
        .\.HIS-EMG\Scripts\activate
        ```
    - using PowerShell
        ```sh
        .\.HIS-EMG\Scripts\Activate.ps1
        ```
    - using Bash
        ```sh
        source .HIS-EMG/bin/activate
        ```

3. Install the requirements and dependancies
    ```sh
    pip install -r requirements.txt
    ```
4. Set Up the Environment Variables in **app.py** file with your own.
    * SECRET_KEY: Is a random secret key used to log sessions.
    * SQLALCHEMY_DATABASE_URI: Is the URI of your database
    


5. Run the application
    ```sh
    python app.py
    ```

6. View the application on localhost
    ```
    http://localhost:5000/
    ```
## Working Demo of the System

You can find a video demo here

```
https://drive.google.com/file/d/1Dk9PFeWPxvGs39YHd3VOY7fn7Nq5KZO0/view
```

## First Entry Information 

Default Admin is created on the first entry, given the following information:
    Name: Creator
    Email: admin@emergency.com
    Password: admin
    Secret Key: ADMIN


## Our Team

* Mostafa Mahmoud - (https://github.com/MostafaAbbas-git)
* Yasser Nasser - (https://github.com/yasser1412)
* Tarek Rashad - (https://github.com/Tarek999)
* Mouaz Hanafy - (https://github.com/Mouaz-hanafy)
* Anas Elahakeam - (https://github.com/AnasElahakeam)



## About
This project is a part of the SBE306 course (Computer Systems 3) in the [Systems and Biomedical Engineering Department - Cairo University]

Dr.Ahmed Kandil\
TA. Ayman Anwar


