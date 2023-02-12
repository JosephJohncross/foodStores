import datetime


def generate_order_number(pk):
    current_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    order_number = current_time + str(pk)
    return order_number