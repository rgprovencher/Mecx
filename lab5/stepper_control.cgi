#!/usr/bin/python37all

import cgi
import cgitb
cgitb.enable()
import json

# # takes in data passed by html page and converts it to a json dictionary
data = cgi.FieldStorage()
settings = {"reset":data.getvalue("reset"), "angle":data.getvalue("angle")}

# writes settings into a text file the bg code can read
with open("step-settings.txt", 'w') as f:
    json.dump(settings, f)
    f.close()
    
    
#rebuilds the html page
print("""Content-type: text/html\n\n
<html>
<br>
<br>

<table width = "100%" border = "0">

<td width = 100 height = 550 text align="center" valign = "top">
    <br>
    <form action = "/cgi-bin/lab5/stepper_control.py" method = "POST">
        <input type="hidden" name="reset" value="0">
        <input type="text" name="angle"> <br>
        <input type="submit" value="set angle">
    </form>    
    <br>
    <form action = "/cgi-bin/lab5/stepper_control.py" method = "POST">
        <input type="hidden" name="reset" value="1">
        <input type="hidden" name="angle" value="0">
        <input type="submit" value="Reset arm to 0">
    </form>
</td>


<td width = 470 height = 550>

    
    
    <iframe width="450" height="260" style="border: 1px solid #cccccc;"
    src="https://thingspeak.com/channels/1554792/charts/1?
    api_key=IBBYTWGOFS0P1EQ7&
    bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=10&
    title=Angle&type=line&xaxis=Time&yaxis=Angle&yaxismax=359&
    yaxismin=0"></iframe>
    <br>
    <iframe width="450" height="260" style="border: 1px solid #cccccc;" 
    src="https://thingspeak.com/channels/1554792/widgets/374774"></iframe>

</td>

</table>

</html>

""")

