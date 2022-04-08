import urllib3
import json

from TrueAccord import TrueAccord

def main():
    http = urllib3.PoolManager()

    debts = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts').data
    payments = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments').data
    plans = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans').data

    debts = json.loads( debts )
    payments = json.loads( payments )
    plans = json.loads( plans )

    result = TrueAccord( debts=debts, payments=payments, plans=plans ).evaluate()
    result = json.dumps( result, indent = 3)

    print( result )



if __name__ == "__main__":
    main()