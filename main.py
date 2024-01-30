import xml.dom.minidom
import os 

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')
file_name = arr[0]
print(file_name)
print(os.path.join(directory, arr[0]))


domtree = xml.dom.minidom.parse(os.path.join(directory, arr[0]))

group = domtree.documentElement
print(group)

loans = group.getElementsByTagName('LOAN')
for loan in loans:
    print(loan.getElementsByTagName('UUID')[0].childNodes[0].nodeValue)
    print(loan.getElementsByTagName('CREDIT_LIMIT')[0].childNodes[0].nodeValue)
    # print(f'-- loan  {loan.getAttribute('UUID')}')
    # print(f'-- loan  {loan.getAttribute('CREDIT_LIMIT')}')


# for child in root: 
#     print(child.tag, child)