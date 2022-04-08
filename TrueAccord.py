from datetime import timedelta, date

from Schedule import Schedule


class TrueAccord:
    def __init__( self, debts = None, payments = None, plans = None ):
        self.debts = debts
        self.payments = payments
        self.plans = plans
        self.result = {}

    def mergeDebtsWithPlans( self ):
        debts = self.debts
        plans = self.plans

        debtWithPlanArray = []

        for d in debts:
            debtWithPlan = {}

            id = d['id']
            amount = d['amount']
            is_in_payment_plan = False

            debtWithPlan['id'] = id
            debtWithPlan['amount'] = amount
            debtWithPlan['is_in_payment_plan'] = is_in_payment_plan

            for p in plans:
                if p['debt_id'] == id:
                    debtWithPlan['is_in_payment_plan'] = True

            debtWithPlanArray.append( debtWithPlan )
        
        self.result = debtWithPlanArray

    def computeRemainingAmount( self ):
        plans = self.plans
        result = self.result
        plans_dict = {}
        new_result = []

        for p in plans:
            startDate = p['start_date']
            frequency = p['installment_frequency']
            amount_to_pay = float( p['amount_to_pay'] )
            installment_amount = p['installment_amount']
            debt_id = p['debt_id']

            increment = 7

            if frequency == "BI_WEEKLY":
                increment = 14

            startDate = str( startDate ).split('-')
            next_date = str( date.today() ).split('-')

            startDate = date( int( startDate[0] ), int( startDate[1] ), int( startDate[2] ) )
            next_date = date( int( next_date[0] ), int( next_date[1] ), int( next_date[2] ) )

            numberOfDays = ( next_date - startDate ).days

            while amount_to_pay >= 0 and numberOfDays >= 7:

                if amount_to_pay == float(0):
                    pass
                
                elif installment_amount > amount_to_pay: #Installment amount is greater than amount remaining. DOnt over pay.
                    installment_amount = amount_to_pay
                    amount_to_pay = amount_to_pay - installment_amount # Will equal zero

                elif installment_amount < amount_to_pay: #Installment amount is less than amount remaining. There's even more to pay.
                    amount_to_pay = amount_to_pay - installment_amount # Will get closer to zero

                elif installment_amount == amount_to_pay: #Exact Installment will finish the payment.
                    amount_to_pay = amount_to_pay - installment_amount # Will equal zero
                    

                #Go to Next week
                numberOfDays = numberOfDays - increment


            #Balance as of today
            p['remaining_amount'] = amount_to_pay
            plans_dict[debt_id] = p

        for r in result:
            id = 1000
            try:
                id = r['id']
                plan = plans_dict[id]
                remaining_amount = plan['remaining_amount']
                r['remaining_amount'] = remaining_amount
                new_result.append( r )
            except KeyError:
                pass

        result = new_result

        return result

    def computeNextDueDate( self ):
        plans = self.plans
        plans_dict = {}
        result = self.result
        new_result = []

        for p in plans:
            startDate = p['start_date']
            frequency = p['installment_frequency']
            debt_id = p['debt_id']

            plans_dict[debt_id] = p

        for r in result:
            id = r['id']

            try:
                plan = plans_dict[id]
                startDate = plan['start_date']
                frequency = plan['installment_frequency']

                next_date = Schedule( startDate=startDate, endDate=date.today(), frequency=frequency ).getNextDueDate()
                next_date = next_date.strftime('%Y-%m-%d')

                r['next_payment_due_date'] = next_date

            except KeyError:
                r['next_payment_due_date'] = None # "null"

            new_result.append( r )

        result = new_result

        return result

    def coalesce( self ):
        result = self.result
        new_result = []


        for r in result:
            try:
                remaining_amount = r['remaining_amount']
            except KeyError:
                remaining_amount = float(0)
                r['remaining_amount'] = remaining_amount
                new_result.append( r )

            if remaining_amount == float(0):
                r['is_in_payment_plan'] = False
                r['next_payment_due_date'] = None

        result = new_result

        return result

    def evaluate( self ):
        self.mergeDebtsWithPlans()

        self.computeRemainingAmount()

        self.computeNextDueDate()

        self.coalesce()

        return self.result
