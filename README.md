# AnaEE
Interface

Prerequisites:
  - Python 3
  - Run "pip install -r requirements.txt" (or "pip3 install -r requirements.txt") to install any required libraries
  
Running:
  - cd to "AnaEE"
  - Execute "python api.py" or "python3 api.py"
  - Open browser and go to URL mentioned in terminal (99% chance it's 127.0.0.1:5000)

Troubleshooting:
  - When you want to update the db and an error occurs you can try to do the following:
     ° Open a terminal and execute following command: rm *.db && rm -r migrations/
    This will remove the current database (ALL INFORMATION WILL BE LOST).
    A new db can be made by running following command: flask db init
    From then on all you (should) need to do is execute following commands every time you want to change the db:
     ° flask db migrate -m "<enter message>"
     ° flask db upgrade