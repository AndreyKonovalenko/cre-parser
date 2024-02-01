import xml.dom.minidom
import os 

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')
# ---person
#<STATUS>00</STATUS> - active
# <OPEN_DATE>12052008</OPEN_DATE>
# <FINAL_PMT_DATE>19052038</FINAL_PMT_DATE>
# <INF_CONFIRM_DATE>31052023</INF_CONFIRM_DATE>
# <TTL_DELQ_5>0</TTL_DELQ_5>
# <TTL_DELQ_5_29>28</TTL_DELQ_5_29>
# <TTL_DELQ_30_59>0</TTL_DELQ_30_59>
# <TTL_DELQ_60_89>0</TTL_DELQ_60_89>
# <TTL_DELQ_30>28</TTL_DELQ_30>
# <TTL_DELQ_90_PLUS>0</TTL_DELQ_90_PLUS>
# <MAX_DELQ_BALANCE>3569.00</MAX_DELQ_BALANCE> - max delay balance
# <DELQ_BALANCE>0.00</DELQ_BALANCE> - dylay current balance
##--- company
# Присутствуют сведения об отрицательной кредитной истории (сработал хотя бы один из критериев):
# - Имеется текущая просроченная задолженность длительностью «0+», более 10 000 руб.;
# - Обнаружен факт возникновения просроченной задолженности по активным счетам длительностью 30 (тридцать) 
# и более календарных дней в кредитных и иных организациях, включая Банк, 
# максимальная сумму просрочки по которым превышала 10 000 руб.;
# Обнаружен факт возникновения просроченной задолженности по закрытыми счетам 
# (дата закрытия счета не превышает 36 месяцев от даты подачи заявки)  длительностью 90 (девяносто) и более календарных дней 
# на сумму более 10 000 руб. в кредитных и иных организациях включая Банк. 


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
        uuid = loan.getElementsByTagName('UUID')
        if uuid.length > 0:
            status = loan.getElementsByTagName('STATUS')
            print(f'uuid: {uuid[0].childNodes[0].nodeValue}')
            print(status.length)
            print(f'status: {status[0].childNodes[0].nodeValue} ') if status.length > 0 else print("status: на задан ")

        # print(loan.getElementsByTagName('UUID')[0].childNodes[0].nodeValue)
        # print(loan.getElementsByTagName('CREDIT_LIMIT')[0].childNodes[0].nodeValue)



for file in arr:
    parser(file)