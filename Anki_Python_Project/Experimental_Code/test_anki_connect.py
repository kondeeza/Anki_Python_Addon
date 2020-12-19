import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


#result = invoke('deckNames')
result = invoke('findCards',  query='"deck:Chinese::Chi 5k Core" rated:30:1 Simplified:瘦 or Key:288')
print(type(result[0]))
print('got list of result: {}'.format(result))  #cid:1423698299436  #cid:1423698299177

# Card types
#CARD_TYPE_NEW = 0
#CARD_TYPE_LRN = 1
#CARD_TYPE_REV = 2
#CARD_TYPE_RELEARNING = 3

# /// col.sched.today.    The number of days that have passed since the collection was created.

"""
 def nextDue(self, c, index):
        if c.odid:
            return tr(TR.BROWSING_FILTERED)
        elif c.queue == QUEUE_TYPE_LRN:
            date = c.due
        elif c.queue == QUEUE_TYPE_NEW or c.type == CARD_TYPE_NEW:
            return tr(TR.STATISTICS_DUE_FOR_NEW_CARD, number=c.due)
        elif c.queue in (QUEUE_TYPE_REV, QUEUE_TYPE_DAY_LEARN_RELEARN) or (
            c.type == CARD_TYPE_REV and c.queue < 0
        ):
            date = time.time() + ((c.due - self.col.sched.today) * 86400)
        else:
            return ""
        return time.strftime(self.time_format(), time.localtime(date))

"""
result = invoke('cardsInfo',  cards=[1423698299436])
print('got list of result: {}'.format(result))
result = invoke('cardsInfo',  cards=[1423698299177])
print('got list of result: {}'.format(result))

result = invoke('areDue',  cards=[1423698299436,1423698299177])
print(result)

result = invoke('getDueDate',  cards=[1423698299436]) #self made api
print(result)

result = invoke('getDueDate',  cards=[1423698299177]) #self made api
print(result)
