import webbrowser
from datetime import datetime

def say_hello_class():
    """
# This code uses the webbrowser module to open the Google homepage in your default web browser. The datetime module is used to obtain the current date and time, and the strftime method is used to format it as a string. The current time is then printed to the console.

    """
url = 'https://www.google.com'
webbrowser.open(url)

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f'The current time is: {current_time}')

