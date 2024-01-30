import xml.dom.minidom
import os 

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')

def parser(file_name: str) -> None:
    print(os.path.join(directory, file_name))
    domtree = xml.dom.minidom.parse(os.path.join(directory, file_name))
    group = domtree.documentElement

    person = group.getElementsByTagName("NAME")
    if (person.length > 0):
        print(group.getElementsByTagName('LAST_NAME')[0].childNodes[0].nodeValue)
    
    business = group.getElementsByTagName('BUSINESS')
    if (business.length > 0):
        print(group.getElementsByTagName('FULL_NAME')[0].childNodes[0].nodeValue)

    loans = group.getElementsByTagName('LOAN')
    for loan in loans:
        print(loan.getElementsByTagName('UUID').length)
        # print(loan.getElementsByTagName('UUID')[0].childNodes[0].nodeValue)
        # print(loan.getElementsByTagName('CREDIT_LIMIT')[0].childNodes[0].nodeValue)



for file in arr:
    parser(file)