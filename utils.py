def isNan(num):
    try:
        int(num)
        return False
    except:
        return True