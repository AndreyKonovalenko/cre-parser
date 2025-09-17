import xml.dom.minidom
import os 
import datetime
import sys
import json
from prettytable import PrettyTable
from constants import *

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')
argTypes = ['scoring', 'short', 'help', 'delay', 'shortTable']

less5 = 'менее 5 дней:'
less29 = 'oт 5 до 29 дней:'
less59 = 'от 30 до 59 дней:'
less89 = 'от 60 до 89 дней:'
plus90 = 'более 90 дней:'

def dateParser(date: str):
    if date: 
      day = date[0:2]
      month = date[2:4]
      year = date[4:]
      parsedDate = datetime.date(int(year), int(month), int(day))
      return parsedDate
    else:
      return 'Дата не задана' 

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
        print(f'{CONFIRM_DATE}: {dateParser(result)}')
    else:
        print(f'{CONFIRM_DATE}: не задана')

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
        return (f'uuid: {uuid}')
    else:
        return ('uuid: не задан')
def uuidHandlerClean(loan):
    uuidTag = loan.getElementsByTagName('UUID')
    if uuidTag.length > 0:
        uuid = uuidTag[0].childNodes[0].nodeValue
        return (uuid)
    else:
        return ('uuid: не задан')
              
def statusHandler(loan):
    result = getElementValueHandler(loan, 'STATUS')
    if result:
        if result == '00':
            return ['00',  'активный']
        if result == '13':
            return ['13', 'закрыт']
        if result == "14":
            return ['14', 'передан на обслуживание в другую организацию']
        if result == '52':
            return ['52', 'просрочен']
    else:
        return ['','не задан']

def currentDelayHandler(loan):
    currentDelay = getElementValueHandler(loan,'CURRENT_DELQ')
    if currentDelay: 
        return currentDelay
    else:
        return None

def pastDueDateHandler(loan):
    pastDueDate= getElementValueHandler(loan, 'PAST_DUE_DATE')
    calculationDate = getElementValueHandler(loan, 'CALCULATION_DATE')
    if pastDueDate and calculationDate: 
        return { "pastDueDate": pastDueDate, "calculationDate": calculationDate}
    else: 
        return None

def creditLimitHandeler(loan):
    creditLimit = getElementValueHandler(loan, 'CREDIT_LIMIT')
    if creditLimit:
        return creditLimit
    else: 
        return None

def productTypeHandler(loan):
    type = getElementValueHandler(loan, 'TYPE')
    if type != None:
      typeText = TYPES.get(type)
      if typeText == None: 
        return "тип " + type + " не описан в объекте TYPES"
      else: 
          return typeText
    else: 
        return "отсутствует tag TYPE"
    
def relationshipTypeHandler(loan):
    relationship = getElementValueHandler(loan, 'RELATIONSHIP')
    if relationship != None:
      typeText = RELATIONSHIPS.get(relationship)
      if typeText == None: 
        return "тип " + relationship + " не описан в объекте RELATIONSHIP"
      else: 
          return typeText
    else: 
        return "отсутвует tag RELATIONSHIP"
    
def currentDelayBalanceHandler(loan):
    currentDelayBalance = getElementValueHandler(loan, 'DELQ_BALANCE')
    if currentDelayBalance:
        return float(currentDelayBalance)
    else: 
        return 0

def maxDelayBalanceHandler(loan):
    result = getElementValueHandler(loan, 'MAX_DELQ_BALANCE')
    if result: 
        return float(result)
    else:
        return 0
       

def termminationReasonHandler(loan):
    result = getElementValueHandler(loan, 'TERMINATION_REASON')
    if result:
        print(f'причина закрытия код: {result}')
        if result == '1':
            print('причина закрытия: ненадлежащее исполнение обязательств')
        if result == '99':
            print('причина закрытия: иное основаение')

def delayInfoHandler(loan):
    result = {
    less5: int(getElementValueHandler(loan, 'TTL_DELQ_5')),
    less29: int(getElementValueHandler(loan,'TTL_DELQ_5_29')),
    less59: int(getElementValueHandler(loan, 'TTL_DELQ_30_59')),
    less89: int(getElementValueHandler(loan, 'TTL_DELQ_60_89')),
    plus90: int(getElementValueHandler(loan, 'TTL_DELQ_90_PLUS')),
    }
    return result

def hasDelay(delay):
    result = False
    for key, value in delay.items():
        if value != 0:
            result = True
            break
    return result

def parser(file_name: str) -> None:
    domtree = xml.dom.minidom.parse(os.path.join(directory, file_name))
    group = domtree.documentElement
    person = group.getElementsByTagName("NAME")

    if (person.length > 0):
      last_name = group.getElementsByTagName('LAST_NAME')[0].childNodes[0].nodeValue
      first_name = group.getElementsByTagName('FIRST_NAME')[0].childNodes[0].nodeValue
      father_name = group.getElementsByTagName('SECOND_NAME')[0].childNodes[0].nodeValue
      print(f"{last_name} {first_name} {father_name}")
    
    business = group.getElementsByTagName('BUSINESS')
    company_OGRN = group.getElementsByTagName('OGRN')[0].childNodes[0].nodeValue if group.getElementsByTagName('OGRN').length> 0 else None
    if (business.length > 0):
        print(f"{group.getElementsByTagName('FULL_NAME')[0].childNodes[0].nodeValue} OGRN: {company_OGRN}")
    
    loans = group.getElementsByTagName('LOAN')
    loans_main_borrower = group.getElementsByTagName('LOANS_MAIN_BORROWER')
    loans_active = group.getElementsByTagName('LOANS_ACTIVE')
    loans_main_borrower_result = loans_main_borrower[0].childNodes[0].nodeValue if loans_main_borrower else "undefined"
    loans_actiev_result = loans_active[0].childNodes[0].nodeValue if loans_active else 'undefined'

    print( f"всего {loans_main_borrower_result} счетов; активных {loans_actiev_result} счетов")

    # delay case only 
 
    table = PrettyTable()
  
    for index, loan in enumerate(loans):
        delay = delayInfoHandler(loan)
        if hasDelay(delay) or getElementValueHandler(loan, 'STATUS') == "52":
            currentDelay = currentDelayHandler(loan)
            pastDueDates=pastDueDateHandler(loan)
            currentDelayBalance = currentDelayBalanceHandler(loan)
            maxDelayBalance = maxDelayBalanceHandler(loan)
            factCloseDate = factCloseDateHandler(loan)
            status = statusHandler(loan)
            creditLimit = creditLimitHandeler(loan)   
            type = productTypeHandler(loan)
            relationship = relationshipTypeHandler(loan)  
           
            if len(sys.argv) < 2:
                print(f'====================N:{index+1}====================')
                print(uuidHandler(loan))
                print(f"статус: {status[1]}")
                print(f'{CREDIT_LIMIT} {creditLimit}')
                print(type + " " + relationship)
                if currentDelay:
                    print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сумму {currentDelayBalance}')
                else:
                    print(f'просроченная задолженность отсутствует')
                print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}')
                termminationReasonHandler(loan)
                confirmDateHandler(loan)
                print('Данные о просрочке:')
                for key, value in delay.items():
                    if value != 0:
                        print(key, value)                    
                if factCloseDate:
                    print(f'{FACT_CLOSE_DATA} {dateParser(factCloseDate)}')
                    delta = timeDeltaHandler(factCloseDate)
                    if delta < 1096:
                        print('с момента закрытия счета прошло менее 3-x лет')
                    else: 
                        print('с момента закрытия счета прошло более 3-x лет')
                print('====================####====================')
                print('')
            # short
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[1]:
                print(uuidHandler(loan) + "; " + f"{status[1]}" + "; " + type + "; " + relationship)
                print(f'{CREDIT_LIMIT} {creditLimit}')
                if currentDelay != None and  currentDelay != '0' or status[0] == '52' :
                    print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сумму {currentDelayBalance} дата возникновения { dateParser(pastDueDates['pastDueDate'] if pastDueDates else None)} дата расчета {dateParser(pastDueDates['calculationDate'] if pastDueDates else None)}')
                else:
                    print(f'просроченная задолженность отсутствует')
                print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}')
                result = ""
                for key, value in delay.items():   
                    if value != 0:
                        result = f"{result} {key} {value};"   
                print(f'Данные о просрочке:{result}')

                if factCloseDate:
                    print(f'{FACT_CLOSE_DATA} {dateParser(factCloseDate)}')
                    delta = timeDeltaHandler(factCloseDate)
                    if delta < 1096:
                        print('с момента закрытия счета прошло менее 3-x лет')
                    else: 
                        print('с момента закрытия счета прошло более 3-x лет')
            # shortTable           
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[4]:
                table.field_names = ["uuid", "лимит", "статус", "макс сумм просрочки", "просрочки", "тип", "дата закрытия", "oтношение"]  
                result = ""
                for key, value in delay.items():   
                    if value != 0:
                        result = f"{result} {key} {value};"                    
                table.add_row([uuidHandlerClean(loan), float(creditLimit), status[1], maxDelayBalance, result, type, str(dateParser(factCloseDate)), relationship])      
            
            # delay 
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[3]:
              table.field_names = ["uuid", "лимит", "статус", "сумма просрочки", "дата воз.", "тип", "oтношение", "дней"]  
              if currentDelay != None and  currentDelay != '0' or status[0] == '52' :
                # tabale.field_names  = ["uuid", "лимит", "статус", "сумма просрочки", "дата воз.", "тип", "oтношение"  "дней"]  
                table.add_row([uuidHandlerClean(loan), creditLimit, status[1], currentDelayBalance, str(dateParser(pastDueDates['pastDueDate'] if pastDueDates else None)), type, relationship, currentDelay])
            
            # scoring          
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[0]:
                currentDelayLogical = currentDelayHandler(loan) and int(currentDelayBalanceHandler(loan)) > 10000
                activeStatus = status[0] == '00' or status[0] == '52'
                delay30to59 = delay[less59] != 0
                delay60to89 = delay[less89] != 0
                delay90Plus = delay[plus90] != 0  

                def deltaHandler():
                    if factCloseDate:
                        if timeDeltaHandler(factCloseDate) < 1096:
                            return True
                    return False
                
                conditionOne = currentDelayLogical and activeStatus
                conditionTwo = activeStatus and (delay30to59 or delay60to89 or delay90Plus) and maxDelayBalance > 10000
                conditionThree = deltaHandler() and maxDelayBalance > 10000 and delay90Plus

                if conditionOne or conditionTwo or conditionThree:
                    print(f'====================N:{index+1}====================')
                    print(uuidHandler(loan))
                    print(f"статус: {status[1]}")
                    print(type + " " + relationship)
                    print(f'{CREDIT_LIMIT} {creditLimit}')
                    confirmDateHandler(loan)
                    print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}') 
                    print('Данные о просрочке:')
                    for key, value in delay.items():
                        if value != 0:
                            print(key, value)

                    if conditionOne:
                        print(f'Имеется {CURRENT_DELAY} длительностью «0+», более 10 000 руб.;')
                        print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сум {currentDelayBalance }')
                        
                    if conditionTwo:
                        print('Обнаружен факт возникновения просроченной задолженности по активным счетам длительностью 30 (тридцать)  и более календарных дней, максимальная сумму просрочки по которым превышала 10 000 руб.')  
                    
                    if conditionThree:
                        print('oбнаружен факт возникновения просроченной задолженности по закрытыми счетам (дата закрытия счета не превышает 36 месяцев от даты подачи заявки)  длительностью 90 (девяносто) и более календарных дней  на сумму более 10 000 руб.')       

                    print('====================####====================')
                    print('')
    if len(sys.argv) > 1 and sys.argv[1] == argTypes[3] or sys.argv[1] == argTypes[4]:
      print(table)
      
    if len(sys.argv) > 2 and (sys.argv[1] == argTypes[3] or sys.argv[1] == argTypes[4]) and sys.argv[2] == 'json':
      json_string = table.get_json_string()
      full_path = os.path.join(directory, f'{company_OGRN if company_OGRN != None else 'output'}.json')
      with open(full_path, 'w') as f:
       f.write(json_string)

if len(sys.argv) == 1: 
  for file in arr:
   parser(file)

if len(sys.argv) > 1:
    if sys.argv[1] == argTypes[2]:
      for element in argTypes:
        print(element)
    if sys.argv[1] != argTypes[2]: 
        for file in arr:
          parser(file)
