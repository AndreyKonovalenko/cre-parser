import xml.dom.minidom
import os 
import datetime
import sys
import json
from prettytable import PrettyTable
from constants import *
import service

directory = os.environ['directory']
arr = os.listdir(rf'{directory}')
argTypes = ['scoring', 'short', 'help', 'delay', 'shortTable']


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

    print( f"всего {loans_main_borrower_result} договоров; активных {loans_actiev_result} договоров")

    # delay case only 
 
    table = PrettyTable()
  
    for index, loan in enumerate(loans):
        delay = service.delayInfoHandler(loan)
        if service.hasDelay(delay) or service.getElementValueHandler(loan, 'STATUS') == "52":
            currentDelay = service.currentDelayHandler(loan)
            pastDueDates=service.pastDueDateHandler(loan)
            currentDelayBalance = service.currentDelayBalanceHandler(loan)
            maxDelayBalance = service.maxDelayBalanceHandler(loan)
            factCloseDate = service.factCloseDateHandler(loan)
            status = service.statusHandler(loan)
            creditLimit = service.creditLimitHandeler(loan)   
            type = service.productTypeHandler(loan)
            relationship = service.relationshipTypeHandler(loan)  
           
            if len(sys.argv) < 2:
                print(f'====================N:{index+1}====================')
                print(service.uuidHandler(loan))
                print(f"статус: {status[1]}")
                print(f'{CREDIT_LIMIT} {creditLimit}')
                print(type + " " + relationship)
                if currentDelay:
                    print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сумму {currentDelayBalance}')
                else:
                    print(f'просроченная задолженность отсутствует')
                print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}')
                service.termminationReasonHandler(loan)
                service.confirmDateHandler(loan)
                print('Данные о просрочке:')
                for key, value in delay.items():
                    if value != 0:
                        print(key, value)                    
                if factCloseDate:
                    print(f'{FACT_CLOSE_DATA} {service.dateParser(factCloseDate)}')
                    delta = service.timeDeltaHandler(factCloseDate)
                    if delta < 1096:
                        print('с момента закрытия договора прошло менее 3-x лет')
                    else: 
                        print('с момента закрытия договора прошло более 3-x лет')
                print('====================####====================')
                print('')
            # short
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[1]:
                print(service.uuidHandler(loan) + "; " + f"{status[1]}" + "; " + type + "; " + relationship)
                print(f'{CREDIT_LIMIT} {creditLimit}')
                if currentDelay != None and  currentDelay != '0' or status[0] == '52' :
                    print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сумму {currentDelayBalance} дата возникновения { service.dateParser(pastDueDates['pastDueDate'] if pastDueDates else None)} дата радоговора {service.dateParser(pastDueDates['calculationDate'] if pastDueDates else None)}')
                else:
                    print(f'просроченная задолженность отсутствует')
                print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}')
                result = ""
                for key, value in delay.items():   
                    if value != 0:
                        result = f"{result} {key} {value};"   
                print(f'Данные о просрочке:{result}')

                if factCloseDate:
                    print(f'{FACT_CLOSE_DATA} {service.dateParser(factCloseDate)}')
                    delta = service.timeDeltaHandler(factCloseDate)
                    if delta < 1096:
                        print('с момента закрытия договора прошло менее 3-x лет')
                    else: 
                        print('с момента закрытия договора прошло более 3-x лет')
            # shortTable           
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[4]:
                table.field_names = ["uuid", "лимит", "статус", "макс сумм просрочки", "просрочки", "тип", "дата закрытия", "oтношение"]  
                result = ""
                for key, value in delay.items():   
                    if value != 0:
                        result = f"{result} {key} {value};"                    
                table.add_row([service.uuidHandlerClean(loan), float(creditLimit), status[1], maxDelayBalance, result, type, str(service.dateParser(factCloseDate)), relationship])      
            
            # delay 
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[3]:
              table.field_names = ["uuid", "лимит", "статус", "сумма просрочки", "дата воз.", "тип", "oтношение", "дней"]  
              if currentDelay != None and  currentDelay != '0' or status[0] == '52' :
                # tabale.field_names  = ["uuid", "лимит", "статус", "сумма просрочки", "дата воз.", "тип", "oтношение"  "дней"]  
                table.add_row([service.uuidHandlerClean(loan), creditLimit, status[1], currentDelayBalance, str(service.dateParser(pastDueDates['pastDueDate'] if pastDueDates else None)), type, relationship, currentDelay])
            
            # scoring          
            if len(sys.argv) > 1 and sys.argv[1] == argTypes[0]:
                currentDelayLogical = service.currentDelayHandler(loan) and int(service.currentDelayBalanceHandler(loan)) > 10000
                activeStatus = status[0] == '00' or status[0] == '52'
                delay30to59 = delay[less59] != 0
                delay60to89 = delay[less89] != 0
                delay90Plus = delay[plus90] != 0  

                def deltaHandler():
                    if factCloseDate:
                        if service.timeDeltaHandler(factCloseDate) < 1096:
                            return True
                    return False
                
                conditionOne = currentDelayLogical and activeStatus
                conditionTwo = activeStatus and (delay30to59 or delay60to89 or delay90Plus) and maxDelayBalance > 10000
                conditionThree = deltaHandler() and maxDelayBalance > 10000 and delay90Plus

                if conditionOne or conditionTwo or conditionThree:
                    print(f'====================N:{index+1}====================')
                    print(service.uuidHandler(loan))
                    print(f"статус: {status[1]}")
                    print(type + " " + relationship)
                    print(f'{CREDIT_LIMIT} {creditLimit}')
                    service.confirmDateHandler(loan)
                    print(f'{MAX_DELAY_BALANCE} {maxDelayBalance}') 
                    print('Данные о просрочке:')
                    for key, value in delay.items():
                        if value != 0:
                            print(key, value)

                    if conditionOne:
                        print(f'Имеется {CURRENT_DELAY} длительностью «0+», более 10 000 руб.;')
                        print(f'{CURRENT_DELAY} {currentDelay} дней/дня на сум {currentDelayBalance }')
                        
                    if conditionTwo:
                        print('Обнаружен факт возникновения просроченной задолженности по активным договорам длительностью 30 (тридцать)  и более календарных дней, максимальная сумму просрочки по которым превышала 10 000 руб.')  
                    
                    if conditionThree:
                        print('oбнаружен факт возникновения просроченной задолженности по закрытыми договорам (дата закрытия договора не превышает 36 месяцев от даты подачи заявки)  длительностью 90 (девяносто) и более календарных дней  на сумму более 10 000 руб.')       

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
