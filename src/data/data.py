import os
import hashlib
import datetime

def get_path():
    paths = os.getcwd().split("\\")
    path = ""
    for index, i in enumerate(paths):
        if index != len(paths) - 1:
            path += i + "/"
    return path

def get_time_now():
    dt = datetime.datetime.now()
    return (dt - datetime.datetime(dt.year, dt.month, dt.day)).total_seconds()
def get_difference_time(first_time, second_time):
    return first_time - second_time#.total_seconds()

def enscrypt_sha256(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def is_in(list_, element):
    return element in list(list_.keys())

def get_int_time():
    dt = datetime.datetime.now()
    return dt.day + dt.hour + dt.minute + dt.second + dt.year + dt.microsecond + dt.month