import webbrowser
import time


time.sleep(20)  # Wait for the server to start
# URL of the webpage you want to open
url = "http://127.0.0.1:5000/plot"

# Open the URL in the default web browser
webbrowser.open(url, new=1)