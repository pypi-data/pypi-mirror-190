import math
import numpy as np
numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}


def extract(string, types=float):
    string = str(string)
    if (str(string) != 'nan'):
        contain_number = False
        num = ""
        for data in string:
            if (data in numbers):
                contain_number = True
                num += data
        if contain_number == True:
            if (types == int):
                return int(math.floor(float(num)))
            else:
                return types(num)
        else:
            return np.nan
    else:
        return np.nan
