def check_of_type(need_type, *variables):
    for i in variables:
        if (need_type == type(i)) == False: return False
    return True