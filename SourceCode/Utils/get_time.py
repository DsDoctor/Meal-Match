from datetime import datetime


def time_now():
    time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')


def time_to_str(t):
    diff_time = time_now() - t
    days = diff_time.days
    t = diff_time.seconds//60//60
    if t == 1:
        hour = str(t) + ' hour'
    else:
        hour = str(t) + ' hours'
    if days == 0:
        return hour
    elif days == 1:
        return '1 day ' + hour
    else:
        return str(days) + ' days ' + hour


def check_exp(user):
    if time_now().day - user.visit_time.day > 0:
        user.max_exp = 0
        user.exp += 5
    user.visit_time = time_now()
    return user


if __name__ == '__main__':
    print(time_now())
    pass
