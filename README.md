Problem set here: https://gist.github.com/jeffling/2dd661ff8398726883cff09839dc316c

To run this, open a terminal, cd into trueaccord

run: python3 main.py

Problem #1: mergeDebtsWithPlans is a simple inner join

Problem #2: RUN python3 TrueAccordUnit.py

Problem #3: computeRemainingAmount

Problem #4: computeNextDueDate 

Problem #5: coalesce
We see that given the payment plan and the dates noted, all paymenrs have expired, thus,
is_in_payment_plan is false for all, next_payment_due_date is null forall and remaining_amount 
is 0.0 for all. This is what the coalesce function handles.
