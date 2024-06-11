Iman Caffe
Introduction
    Iman caffe is a simple online shopping web app where users sign up, browse items, add items to their cart and checkout.
    Other features include:managing your account, receiving mail for confirmation
    Here's the link to the deployed web app: https://imaan-caffe-f7f987595df4.herokuapp.com/
    Authors:
        Adnan Gard Obuya - https://www.linkedin.com/in/adnan-obuya-9bb70a289/
    Blog posts:
        After succesfully deploying the web app,I wrote a blog post to reflect on the Iman Caffe web app journey.
        Adnan's article - https://medium.com/@gardobuyaadnan/a-simple-online-shopping-web-app-972e3abe59ac
Installation
    First,you clone this repo,then navigate to the app.py python file.Before running the python file using the command python3 app.py, you'll first need to install the necessary programms required to run the app.
    For linux users,ensure that the latest version of python3 is installed in your computer,if not,you can do so by running the cmd: sudo apt install python3.
    You'll also need to ensure that the flask module is installed.Do so by running the cmd:pip3 install flask.
    For sending and receiving mail between the customer and owner(in this case you), you need to head over to Mailgun and create an account to receive the SMTP server, port username and password.Note that without these crutial info, you wont be able to use this feature.
    In order to also run this web app in your local machine,you'll also need to modify some code in the database.py located in the models.engine folder.In the def __init__(self) method,replace the existing code with:self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(mysql_user,mysqlpswd,mysql_hst,mysql_db)).The mysql_user,pswd,hst,db are all variables that contain actual details of your database.
    Finally before running the app.py,run the instances.py to add items to the database.

Usage
    If your a new user,you just sign up in the home page sign up page option.Next ou login and you'll be redirected to the menu.Following that,you could add items to the cart and choose to sign out.

Contributing
    1. **Fork the Repository**
   - Navigate to the top right of this repository and click the "Fork" button to create a copy of the repository under your GitHub account.

    2. **Clone the Repository**
    Clone your forked repository to your local machine:
     ```sh
     git clone https://github.com/your-username/your-repo-name.git
     ```
    Replace `your-username` and `your-repo-name` with your GitHub username and the repository name.

    3. **Create a Branch**
    Create a new branch for your changes:
     ```sh
     git checkout -b feature/your-feature-name
     ```
    Use a descriptive name for your branch that clearly indicates the purpose of the changes.

    4. **Make Changes**
    Make your changes to the codebase.
    Follow the project's coding style and guidelines.

    5. **Commit Your Changes**
    Commit your changes with a descriptive commit message:
     ```sh
     git commit -m "Add feature: description of your feature"
     ```

    6. **Push to Your Fork**
    Push your changes to your forked repository:
     ```sh
     git push origin feature/your-feature-name
     ```

    7. **Create a Pull Request**
    Navigate to the original repository and click the "New pull request" button.
    Provide a clear and descriptive title for your pull request.
    Describe the changes you have made and any relevant information in the pull request description.

Related Projects
    The landing page to the created web app: https://github.com/Adnangad/landing_page

Licensing
    MIT License