# Online-Job-Application System (Full stack web Application)
Welcome to the Online Job Application System! This system allows applicants to seamlessly apply for jobs via the internet, and provides employers with the tools to manage job postings and applicants efficiently. Below is an overview of the repository structure and the functionality offered by the system.

##### Repository Structure
.
├── models/ (contains all models)
│   └── applications(contains all application related data)
    |___jobs(contains all jobs detail)
    |___sign_up(contains applicants detail,)
    |___user(contains admin usesr information)
├── templates/
│   └── ... (contains all HTML code)
├── static/
│   ├── scripts/(contains all java script files)
│   ├── styles/(contains all css codes)
│   └── images/(contains all image)
│       └── ... (contains all static files)
|__ requirements.txt---contains all the required packages and libraries
├── app.py (contains all API endpoint routes)
└── README.md


###### Folders and Files
#### models/: 
This directory contains all the data models used in the application, such as user, job,sign_up, and application models.
#### templates/: 
This directory holds all the HTML templates used for rendering web pages.
#### static/scripts/: 
Contains all JavaScript files used in the application.
#### static/styles/: 
Contains all CSS files for styling the application.
#### static/images/:
 Contains all image files used in the application.
#### app.py: 
The main application file which includes all API endpoint routes and core functionality.

### Features
#### For Applicants
#### Sign Up: 
Allows new users to register for an account.
#### Sign In: 
Allows registered users to log in using their email and password.
#### Profile View: 
Enables applicants to view and update their profile information.
#### Job Application: 
Permits registered users to apply for available jobs.
prevents applicants from sending more than one application using one email
#### Application Status: 
Allows users to view the status of their job applications.

### For Employers
#### Manage Jobs: 
Employers can view, search, post, update, and manage job listings.
#### Applicant Management: 
Employers can view applicants, filter applicants by job ID, and manage applicant information.
#### User Management: 
Employers can view registered users and add, update, or remove admin users.

### Additional Functionality
#### Job Expiry: 
The system checks the due date of job postings and automatically removes jobs from the home page once the due date has passed.

### Getting Started
To get started with the development or deployment of the Online Job Application System, follow these steps:

#### 1. Clone the Repository:

    git clone https://github.com/bekiyeromm/online-job-application.git

#### 2. Install Dependencies:
Navigate to the project directory and install the required dependencies.

    cd online-job-application
    pip install -r requirements.txt

#### Run the Application:
Start the application by running the following command.

    python3 app.py

#### 4. Access the Application:
Open your web browser and navigate to http://localhost:5000 or http://http://127.0.0.1:5000/ to access the system.

#### Contribution
Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request.

#### License
This project is free, no copy right protection. you can download use for free.

Thank you for using the Online Job Application System! For any questions or support, please contact at:<br>
 <a href="mailto:bk3tena@gmail.com">Email</a>.<br>
<a href="https://www.linkedin.com/in/bereket-tena-43a171125/">Linkedin</a><br>
<a href ="https://github.com/bekiyeromm">Git hub</a><br>
<a href = "https://twitter.com/BereketTena1"> Twitter</a><br>
<a href = "https://www.youtube.com/channel/UC64xIrygGM3BMs4N73VXm5Q">You Tube</a><br>

This README file provides a concise overview of the project and its functionality. It is portfolio project for graduation specialization in back-end  @ALX Africa/ Holberton School.