import datetime


# return whether it's the weekend or not
def the_weekend():
    weekno = datetime.datetime.today().weekday()

    if weekno < 5:
        # this is weekday: 0-4
        return 0
    else:
        return 1
