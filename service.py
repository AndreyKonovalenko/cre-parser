import datetime
from constants import *
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
