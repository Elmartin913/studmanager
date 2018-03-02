import datetime


def my_cp(request):
    ctx = {
        'date': datetime.date.today(),
        'version': 'v.6.3.7'
    }
    return ctx
