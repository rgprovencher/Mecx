#!/usr/bin/python37all

import cgi
import cgitb
cgitb.enable()
import json

# # takes in data passed by html page and converts it to a json dictionary
data = cgi.FieldStorage()
settings = {"reset":data.getalue("reset"), "angle":data.getvalue("angle")}

# writes settings into a text file the bg code can read
with open("step-settings.txt", 'w') as f:
    json.dump(settings, f)
    
    
# rebuilds the html page
print("""Content-type: text/html\n\n
<html>
<br>
<br>
<form action = "cgi-bin/lab5/stepper_control.py" method = "POST">
    <input type="hidden" name="reset" value="0">
    <input type="text" name="angle">
</form>    
<br>
<form action = "cgi-bin/lab5/stepper_control.cgi" method = "POST">
    <input type="hidden" name="reset" value="1">
    <input type="hidden" name="angle" value="0">
    <input type="submit" value="Reset arm to 0">
</form>

</html>

""")