from xml.dom import minidom
# xmldoc = minidom.parse('t1.xml')
xmldoc = minidom.parse('t34059.xml')
itemlist = xmldoc.getElementsByTagName('Y')

for s in itemlist:
    print(f"{s.attributes['t'].value}: {s.childNodes[0].data}")