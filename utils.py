from passlib.hash import pbkdf2_sha256

from models.timeframes import Timeframes


def hash_password(password):
    return pbkdf2_sha256.hash(password)


def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)


def check_admin(password):
    admin_pass = 123
    if admin_pass == password:
        return True
    else:
        return False


def check_email(email):
    if email.endswith('turkuamk.fi'):
        return True
    else:
        return False


def check_timeframes(timeframe1, timeframe2, workspace_number):
    initial_timeframe_list = Timeframes.get_all(workspace_number)
    timeframe_list = []

    # remove timeframes from different months and days
    for timeframe in initial_timeframe_list:
        if timeframe.start_time.month == timeframe1.month and timeframe.start_time.day == timeframe1.day:
            timeframe_list.append(timeframe)

    # if list is empty returns True
    if timeframe_list is None:
        return None

    # check if the timeframe is available and if not, give recommendations
    else:
        for tframe in timeframe_list:
            if tframe.start_time <= timeframe1 <= tframe.end_time or tframe.start_time <= timeframe2 <= tframe.end_time:
                return "There is a meeting between {}:{} and {}:{}, try a different time frame".format(
                    tframe.start_time.hour,
                    tframe.start_time.minute,
                    tframe.end_time.hour,
                    tframe.end_time.minute)
        return None



