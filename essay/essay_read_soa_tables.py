from xml.dom import minidom

http_header = 'https://mort.soa.org/ViewTable.aspx?&TableIdentity='
xmldoc = minidom.parse('../soa_tables/CSO_1941.xml')
xmldoc = minidom.parse('../soa_tables/GRF95.xml')
# xmldoc = minidom.parse('TV8890.xml')
table_id = xmldoc.getElementsByTagName('TableIdentity')[0].childNodes[0].data
url = http_header + table_id

name = xmldoc.getElementsByTagName('TableName')[0].childNodes[0].data
contentType = xmldoc.getElementsByTagName('ContentType')[0].childNodes[0].data
tableReference = xmldoc.getElementsByTagName('TableReference')[0].childNodes[0].data
ages = xmldoc.getElementsByTagName('Y')

min_age = int(ages[0].attributes['t'].value)
max_age = min_age + len(ages) - 1

print(f"Preparing table {name} with minimum age {min_age} and maximum age {max_age}\n{url}")
table_qx = [float(age.childNodes[0].data) for age in ages]
table_qx.insert(0, min_age)

'''
for age in ages:
    print(f"{age.attributes['t'].value}: {age.childNodes[0].data}")
'''
