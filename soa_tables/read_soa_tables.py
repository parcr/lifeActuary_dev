from urllib.request import urlopen
response = urlopen('https://mort.soa.org/data/t1.xml')
html = response.read()
print(html)
