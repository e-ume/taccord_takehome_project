import unittest
import urllib3
import json
import warnings


from TrueAccord import TrueAccord


class TestStringMethods(unittest.TestCase):
    def setup( self ):
        http = urllib3.PoolManager()

        debts = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/debts').data
        payments = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payments').data
        plans = http.request('GET', 'my-json-server.typicode.com/druska/trueaccord-mock-payments-api/payment_plans').data

        debts = json.loads( debts )
        payments = json.loads( payments )
        plans = json.loads( plans )

        result = TrueAccord( debts=debts, payments=payments, plans=plans ).evaluate()

        return result

    def test_ID_4_PaymentPlan(self):
        warnings.simplefilter("ignore", ResourceWarning)
        data = self.setup()
        is_in_payment_plan = data[4]['is_in_payment_plan']
        self.assertEqual( is_in_payment_plan, False )


    def test_ID_2_PaymentPlan(self): 
        warnings.simplefilter("ignore", ResourceWarning)
        data = self.setup()
        is_in_payment_plan = data[2]['is_in_payment_plan']
        self.assertEqual( is_in_payment_plan, False )

    def test_ID_4_DueDateNull(self): 
        warnings.simplefilter("ignore", ResourceWarning)
        data = self.setup()
        next_payment_due_date = data[4]['next_payment_due_date']
        self.assertEqual( next_payment_due_date, None )

if __name__ == '__main__':
    unittest.main()