from datetime import timedelta, date

class Schedule:
    def __init__( self, startDate = None, endDate = None, frequency = None ):
        self.startDate = startDate
        self.endDate = endDate
        self.frequency = frequency

    def getNextDueDate( self ):
        startDate = str( self.startDate ).split('-')
        endDate = str( self.endDate ).split('-')
        frequency = self.frequency

        startDate = date( int(startDate[0]), int(startDate[1]), int(startDate[2]) )
        endDate = date( int(endDate[0]), int(endDate[1]), int(endDate[2]) )

        numberOfDays = ( endDate - startDate ).days

        daysToNextDueDate = 0
        daysFromLastDueDate = 0
        nextDueDate = ''

        if frequency == "WEEKLY":
            daysFromLastDueDate = numberOfDays % 7
            lastDueDate = endDate - timedelta( days=daysFromLastDueDate )
            nextDueDate = lastDueDate + timedelta( days=7 )
        else:
            daysFromLastDueDate = numberOfDays % 14
            lastDueDate = endDate - timedelta( days=daysFromLastDueDate )
            nextDueDate = lastDueDate + timedelta( days=14 )

        return nextDueDate
