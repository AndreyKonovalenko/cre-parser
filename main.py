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

# <DELQ_BALANCE>0.00</DELQ_BALANCE> - delay current balance
# <CURRENT_DELQ>0</CURRENT_DELQ> - current delay
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
        uuidTag = loan.getElementsByTagName('UUID')
        statusTag = loan.getElementsByTagName('STATUS')
        currentDelayTag = loan.getElementsByTagName('CURRENT_DELQ')
        currentDelayBalanceTag = loan.getElementsByTagName('DELQ_BALANCE')
        delayLess5 = loan.getElementsByTagName('TTL_DELQ_5')[0].childNodes[0].nodeValue
        delay5to29 = loan.getElementsByTagName('TTL_DELQ_5_29')[0].childNodes[0].nodeValue
        delay30to59 = loan.getElementsByTagName('TTL_DELQ_30_59')[0].childNodes[0].nodeValue
        delay60to89 = loan.getElementsByTagName('TTL_DELQ_60_89')[0].childNodes[0].nodeValue
        delay90Plus = loan.getElementsByTagName('TTL_DELQ_90_PLUS')[0].childNodes[0].nodeValue

        if uuidTag.length > 0:
            uuid = uuidTag[0].childNodes[0].nodeValue
            print(f'uuid: {uuid}')
        else:
            print(f'uuid: не задан')
            
        if statusTag.length > 0:
            status = statusTag[0].childNodes[0].nodeValue
            print(status) 
            if status == '00':
                print('активный')
            if status == '13':
                print('закрыт')
        else:
            print("cтатус: на задан ")

        if (currentDelayTag.length > 0):
            currentDelay = currentDelayTag[0].childNodes[0].nodeValue
            currentDelayBalance = "0.00"
            if(currentDelayBalanceTag.length > 0):
                currentDelayBalance = currentDelayBalanceTag[0].childNodes[0].nodeValue
            print(f'текущая просрочка дней: {currentDelay} дней, на сумму: {currentDelayBalance} ')
        else:
            print('просроченная задолженность отсутствует')

       
        if delayLess5 != '0' or delay5to29 != '0' or delay30to59 != '0' or delay60to89 != '0' or delay90Plus != '0':
            print('Данные о просрочке:')
            if delayLess5 != '0': print(f'менее 5 дней: {delayLess5}')
            if delay5to29 != '0': print(f'5-29 дней: {delay5to29}')
            if delay30to59 != '0': print(f'30-59 дней: {delay30to59}')
            if delay60to89 != '0': print(f'60-89: {delay60to89}')
            if delay90Plus != '0': print(f'Более 90: {delay90Plus}')
        else: 
            print('Историческая просрочка не обнаружена')

        # print(loan.getElementsByTagName('UUID')[0].childNodes[0].nodeValue)
        # print(loan.getElementsByTagName('CREDIT_LIMIT')[0].childNodes[0].nodeValue)


for file in arr:
    parser(file)