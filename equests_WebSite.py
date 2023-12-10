import urequests
r = urequests.get('http://www.jab.tw/')
print(r.content)
r.close()