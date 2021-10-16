#!/usr/bin/python373all
import cgi

print("Content-type: text/html\n\n")
data = cgi.FieldStorage()
print("selection = " + data.getvalue('two_buttons'))
