#!/usr/bin/python37all

# Save file as /usr/lib/cgi-bin/test.py

print('Content-type:text/html\n\n’)
print('<html><body>')
print('<form action="/cgi-bin/test.py" method="POST"')
print('<input type="submit" value="create a new page">')
print('</form>')
print('</body></html>')