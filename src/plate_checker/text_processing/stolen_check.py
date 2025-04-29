import random as r

def stolen(licenseplate):
    num= r.randint(1,10000)
    if num <=25:
        return True
    else:
        return False
    