import re

# Most of this is shamelessly taken from TyMick. Ty, Mick.
def num(n):
    try:
        return int(n)
    except:
        try:
            return float(n)
        except:
            return None


def get_num(input):
    # Split at first letter
    index_to_split = re.search(r"[A-Za-z]", input).start()
    if index_to_split == 0:
        return 1
    elif index_to_split:
        num_string = input[0:index_to_split]
    else:
        num_string = input

    # Check for fraction
    fraction_match = re.search(r"^(\d*\.?\d*)\/(\d*\.?\d*)$", num_string)
    if fraction_match:
        try:
            return num(num(fraction_match.group(1)) / num(fraction_match.group(2)))
        except:
            return None

    return num(num_string)


def get_unit(input):
    # Split at first letter
    index_to_split = re.search(r"[A-Za-z]", input).start()
    if index_to_split is not None:
        unit_string = input[index_to_split : len(input)]
    else:
        return None

    if re.search(r"^(gal|L|lbs|kg|mi|km)$", unit_string, re.I):
        if re.search(r"^L$", unit_string, re.I):
            return unit_string.upper()
        else:
            return unit_string.lower()
    else:
        return None


def get_return_unit(init_unit):
    return_units = {
        "gal": "L",
        "L": "gal",
        "lbs": "kg",
        "kg": "lbs",
        "mi": "km",
        "km": "mi",
    }
    return return_units.get(init_unit)


def spell_out_unit(unit):
    spelled_out_units = {
        "gal": "gallons",
        "L": "liters",
        "lbs": "pounds",
        "kg": "kilograms",
        "mi": "miles",
        "km": "kilometers",
    }
    return spelled_out_units.get(unit)


def convert(init_num, init_unit):
    if init_num is None:
        return None

    GAL_TO_L = 3.78541
    LBS_TO_KG = 0.453592
    MI_TO_KM = 1.60934

    if init_unit == "gal":
        return round(init_num * GAL_TO_L, 5)
    elif init_unit == "L":
        return round(init_num / GAL_TO_L, 5)
    elif init_unit == "lbs":
        return round(init_num * LBS_TO_KG, 5)
    elif init_unit == "kg":
        return round(init_num / LBS_TO_KG, 5)
    elif init_unit == "mi":
        return round(init_num * MI_TO_KM, 5)
    elif init_unit == "km":
        return round(init_num / MI_TO_KM, 5)
    else:
        return None


def get_string(init_num, init_unit, return_num, return_unit):
    if init_num is None:
        if init_unit is None:
            return "Invalid number and unit"
        else:
            return "Invalid number"
    elif init_unit is None:
        return "Invalid unit"
    else:
        return (
            str(init_num)
            + " "
            + spell_out_unit(init_unit)
            + " converts to "
            + str(return_num)
            + " "
            + spell_out_unit(return_unit)
        )

# Handles conversion when provided string
def convertHandler(message):
    num = get_num(message)
    unit = get_unit(message)
    returnUnit = get_return_unit(unit)
    convertedNum = convert(num,unit)
    result = get_string(num,unit,convertedNum,returnUnit)
    return str(result)