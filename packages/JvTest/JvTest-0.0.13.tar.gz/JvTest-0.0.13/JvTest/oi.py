import requests

def Oioi():
  r = requests.get("http://google.com").text
  print(r)