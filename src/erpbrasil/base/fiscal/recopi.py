# coding=utf-8
# Copyright (C) 2023  Daniel Venancio - KMEE
# License MIT - See https://opensource.org/license/mit
import datetime as dt

CURRENT_YEAR = dt.date.today().year
CURRENT_MONTH = dt.date.today().month
CURRENT_DAY = dt.date.today().day
VERIFICATION_DIGIT_WEIGHT = [
    19,
    18,
    17,
    16,
    15,
    14,
    13,
    12,
    11,
    10,
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
]


def is_valid_recopi(recopi):
    if _check_recopi_size(recopi):
        if _check_recopi_format(recopi):
            return True
    return False


def generate_valid_recopi():
    recopi_date = _generate_recopi_date()
    recopi_hour = _generate_recopi_hour()
    recopi_four_digits = _generate_recopi_four_digits()
    recopi_verification_digits = _generate_recopi_verification_digits(
        recopi_date + recopi_hour + recopi_four_digits
    )
    recopi = recopi_date + recopi_hour + recopi_four_digits + recopi_verification_digits
    return recopi


def _check_recopi_size(recopi):
    if len(recopi) == 20:
        return True
    return False


def _check_recopi_format(recopi):
    return (
        _check_recopi_date(recopi)
        and _check_recopi_time(recopi)
        and _check_recopi_verification_digits(recopi)
    )


def _check_recopi_date(recopi):
    recopi_year, recopi_month, recopi_day = get_recopi_date(recopi)
    try:
        dt.date(
            year=recopi_year, month=recopi_month, day=recopi_day
        )  # _check if it's a calendar date
        if recopi_year > CURRENT_YEAR:
            return True
        elif recopi_year == CURRENT_YEAR and recopi_month > CURRENT_MONTH:
            return True
        elif recopi_year < 2013:
            return True

        return False
    except:
        return False


def get_recopi_date(recopi):
    recopi_year = int(recopi[0:4])
    recopi_month = int(recopi[4:6])
    recopi_day = int(recopi[6:8])
    return recopi_year, recopi_month, recopi_day


def _check_recopi_time(recopi):
    recopi_hour, recopi_minute, recopi_second = get_recopi_time(recopi)
    try:
        dt.datetime(
            year=2003,
            month=4,
            day=21,
            hour=recopi_hour,
            minute=recopi_minute,
            second=recopi_second,
        )
        return True
    except:
        return False


def get_recopi_time(recopi):
    recopi_hour = int(recopi[8:10])
    recopi_minute = int(recopi[10:12])
    recopi_second = int(recopi[12:14])
    return recopi_hour, recopi_minute, recopi_second


def _check_recopi_verification_digits(recopi):
    return _check_recopi_first_verification_digit(
        recopi
    ) and _check_recopi_second_verification_digit(recopi)


def _check_recopi_first_verification_digit(recopi):
    if calculate_first_verification_digit(recopi) == int(recopi[18]):
        return True
    return False


def calculate_first_verification_digit(recopi):
    sum = 0
    for count in range(0, 18):
        sum = sum + (int(recopi[count]) * VERIFICATION_DIGIT_WEIGHT[count + 1])
    return 11 - (sum % 11)


def _check_recopi_second_verification_digit(recopi):
    if calculate_second_verification_digit(recopi) == int(recopi[19]):
        return True
    return False


def calculate_second_verification_digit(recopi):
    sum = 0
    for count in range(0, 19):
        sum = sum + (int(recopi[count]) * VERIFICATION_DIGIT_WEIGHT[count])
    return 11 - (sum % 11)


def _generate_recopi_date():
    return str(CURRENT_YEAR + 1) + "0101"


def _generate_recopi_hour():
    return "080000"


def _generate_recopi_four_digits():
    return "1234"


def _generate_recopi_verification_digits(inicial_digits):
    first_verification_digit = str(calculate_first_verification_digit(inicial_digits))
    second_verification_digit = str(
        calculate_second_verification_digit(inicial_digits + first_verification_digit)
    )

    return first_verification_digit + second_verification_digit
