import xml.dom.minidom
import os 
import datetime
import sys

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')
argTypes = ['scoring']

def dateParser(date: str):
    day = date[0:2]
    month = date[2:4]
    year = date[4:]
    parsedDate = datetime.date(int(year), int(month), int(day))
    return parsedDate

def timeDeltaHandler(close):
    startDate = dateParser(close)
    now = datetime.date.today()
    delta = now - startDate
    return delta.days

def getElementValueHandler(loan, type):
    elementTag = loan.getElementsByTagName(type)
    if(elementTag.length > 0):
        return elementTag[0].childNodes[0].nodeValue
    else:
        return None

def confirmDateHandler(loan):
    result = getElementValueHandler(loan, 'INF_CONFIRM_DATE')
    if result:
        print(f'дата подтверждения: {dateParser(result)}')
    else:
        print("дата подтверждения: не задана")

def factCloseDateHandler(loan):
    result = getElementValueHandler(loan, 'FACT_CLOSE_DATE')
    if result:
        return result
    else:
        return None

def uuidHandler(loan):
    uuidTag = loan.getElementsByTagName('UUID')
    if uuidTag.length > 0:
        uuid = uuidTag[0].childNodes[0].nodeValue
        print(f'uuid: {uuid}')
    else:
        print('uuid: не задан')
            
def statusHandler(loan):
    result = getElementValueHandler(loan, 'STATUS')
    if result:
        if result == '00':
            return ['00',  'активный']
        if result == '13':
            return ['13', 'закрыт']
        if result == "14":
            return ['14', 'передан на обслуживание в другую организацию']
        if result == "52":
            return ['52', 'просрочен']
    else:
        return ['','не задан']

def currentDelayHandler(loan):
    currentDelay = getElementValueHandler(loan,'CURRENT_DELQ')
    if currentDelay: 
        return currentDelay
    else:
        return   None

def currentDelayBalanceHandler(loan):
    currentDelayBalance = getElementValueHandler(loan, 'DELQ_BALANCE')
    if currentDelayBalance:
        return float(currentDelayBalance)
    else: 
        return 0

def maxDeleyBalanceHandler(loan):
    result = getElementValueHandler(loan, 'MAX_DELQ_BALANCE')
    if result: 
        return float(result)
    else:
        return 0
       

def termminationReasonHandler(loan):
    result = getElementValueHandler(loan, 'TERMINATION_REASON')
    if result:
        print(f'причена закрытия код: {result}')
        if result == '1':
            print('причина закрытия: ненадлежащее исполнение обязательств')
        if result == '99':
            print('причина закрытия: иное основаение')

def delayInfoHandler(loan):
    result = {
    'менее 5 дней:': int(getElementValueHandler(loan, 'TTL_DELQ_5')),
    'от 5 до 29 дней:': int(getElementValueHandler(loan,'TTL_DELQ_5_29')),
    'от 30 до 59 дней:': int(getElementValueHandler(loan, 'TTL_DELQ_30_59')),
    'от 60 до 89 дней:': int(getElementValueHandler(loan, 'TTL_DELQ_60_89')),
    'более 90 дней:': int(getElementValueHandler(loan, 'TTL_DELQ_90_PLUS')),
    }
    return result

def hasDelay(dalay):
    result = False
    for key, value in dalay.items():
        if value != 0:
            result = True
            break
    return result

def parser(file_name: str) -> None:
    domtree = xml.dom.minidom.parse(os.path.join(directory, file_name))
    group = domtree.documentElement
    person = group.getElementsByTagName("NAME")

    print('/n')

    if (person.length > 0):
        print(group.getElementsByTagName('LAST_NAME')[0].childNodes[0].nodeValue)
    
    business = group.getElementsByTagName('BUSINESS')
    if (business.length > 0):
        print(group.getElementsByTagName('FULL_NAME')[0].childNodes[0].nodeValue)

    loans = group.getElementsByTagName('LOAN')

    for index, loan in enumerate(loans):
        delay = delayInfoHandler(loan)
        if hasDelay(delay):
            currentDelay = currentDelayHandler(loan)
            currentDelayBalance = currentDelayBalanceHandler(loan)
            maxDeleyBalance = maxDeleyBalanceHandler(loan)
            factCloseDate = factCloseDateHandler(loan)
            status = statusHandler(loan)     
            print(f'====================N:{index+1}====================')
            if len(sys.argv) < 2:
                uuidHandler(loan)
                print(f"статус: {status[1]}")
                if currentDelay:
                    print(f'текущая просроченная задолженнсоть {currentDelay} дней/дня на сумму {currentDelayBalance}')
                else:
                    print(f'просроченная задолженность отсутвует')
                print(f'максимальяная сумма просроченнйо задолженности {maxDeleyBalance}')
                termminationReasonHandler(loan)
                confirmDateHandler(loan)
                print('Данные о просрочке:')
                for key, value in delay.items():
                    if value != 0:
                        print(key, value)                    
                if factCloseDate:
                    print(f'дата закртыия счета {dateParser(factCloseDate)}')
                    delta = timeDeltaHandler(factCloseDate)
                    if delta < 1096:
                        print('с момента закрытия счета прошло менее 3-x лет')
                    else: 
                        print('с момента закрытия счета прошло более 3-x лет')
                        
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[0]:
                # main data:
                uuidHandler(loan)
                currentDelayLogical = currentDelayHandler(loan) and int(currentDelayBalanceHandler(loan)) > 10000
                activeStatus = status[0] == '00' or status[0] == '52'
                delay30Plus = delay['менее 5 дней:'] != 0;
                
                if (currentDelayHandler(loan)) and int(currentDelayBalanceHandler(loan)) > 10000 and (status[0] == '00' or status[0] == '52') :
                    print('Имеется текущая просроченная задолженность длительностью «0+», более 10 000 руб.;')
                    print(f'текущая просроченная задолженнсоть {currentDelay} дней/дня на сум {currentDelayBalance }')
              
                    
            print('====================####====================')
            print('')

for file in arr:
    parser(file)


# Присутствуют сведения об отрицательной кредитной истории (сработал хотя бы один из критериев):
# - Имеется текущая просроченная задолженность длительностью «0+», более 10 000 руб.;
# - Обнаружен факт возникновения просроченной задолженности по активным счетам длительностью 30 (тридцать) 
# и более календарных дней в кредитных и иных организациях, включая Банк, 
# максимальная сумму просрочки по которым превышала 10 000 руб.;
# Обнаружен факт возникновения просроченной задолженности по ызакрытыми счетам 
# (дата закрытия счета не превышает 36 месяцев от даты подачи заявки)  длительностью 90 (девяносто) и более календарных дней 
# на сумму более 10 000 руб. в кредитных и иных организациях включая Банк. 

