from mimetypes import init
import re

# This script is based on one from github.com/TyMick. Ty, Mick.

''' 
Convert.py is responsible for parsing strings (messages) and converting any found units, then returning responses with them as an array.

TODO split this up into more sensible script files
Separate files for:
- Control unit file - Takes string input from bot.py and handles using the rest of the files, before returning result back to bot.py 
- Parsing file - Extracts measurements
- Conversion file - Converts numbers and measurements to whatever opposite is pre-determined
- Formatting file - Formats a reply string to be posted in discord
'''

return_units = { # Which unit converts to what
        "f" : "c",
        "c" : "f",
        "gal": "L",
        "L": "gal",
        "lbs": "kg",
        "kg": "lbs",
        "lb": "kg",
        "mi": "km",
        "km": "mi",
        "cm" : "in",
        "in" : "cm",
        "ft" : "m",
        "m" : "ft",
        "mm" : "in",
        "kph" : "mph",
        "mph" : "kph",
        "kmh" : "mph"
}

spelled_out_units = { # Full names and short names
        "gal": "gallons",
        "L": "liters",
        "lbs": "pounds",
        "lb": "pound",
        "kg": "kilograms",
        "mi": "miles",
        "km": "kilometers",
        "cm" : "centimeters",
        "in" : "inches",
        "ft" : "feet",
        "m" : "meters",
        "f" : "fahrenheit",
        "c" : "celsius",
        "mm" : "millimeters",
        "kph" : "Kilometers per hour",
        "kmh" : "Kilometers per hour",
        "mph" : "Miles per hour"
}

def num(n):
    try:
        return int(n)
    except:
        try:
            return float(n)
        except:
            return None

# Attempts to strip message to only number and unit. Big and messy
# First find index where unit starts
def strip_msg(input, maxResponses):
    converted = []
    for i in range(maxResponses): # Limit number of parsed messages to a custom/sensible number
        number,wordIndex = get_num_strip(input)
        if isinstance(number, int) or isinstance(number, float):
            unit,toRemove = get_unit_strip(input,wordIndex)
            print(unit)
            unit = re.sub("[^a-zA-Z]+", "", unit)
            print(unit)
            if unit == None:
                break
            elif unit == "l":
                if "-" in str(number) and unit.lower() not in ["fahrenheit", "f", "celsius", "c"]:
                    number = num(str(number).strip("-"))
                converted.append([number,unit.upper()])
            
                input = input.replace(str(number), "", 1) # Remove already converted/extracted
                input = input.replace(toRemove, "", 1) # Remove already converted/extracted
            else:
                if "-" in str(number) and unit.lower() not in ["fahrenheit", "f", "celsius", "c"]:
                    number = num(str(number).strip("-"))
                converted.append([number,unit])
            
                input = input.replace(str(number), "", 1) # Remove already converted/extracted
                input = input.replace(toRemove, "", 1) # Remove already converted/extracted
        else:
            break

    return converted

# Strip before number, using index of unit
def get_num_strip(input):
    # Split at first number followed by a letter
    try: 
        indexFirstLetter = re.search(r"\d\s[A-Za-z]|\d[A-Z[a-z]", input).start()
    except:
        return None,None

    stripInput = ""
    if input[indexFirstLetter+1] == " ": # Strip to first letter after number and space
        indexFirstLetter += 2
        stripInput = input[0:indexFirstLetter] 
    else:                              # Or strip to with no space between num and letter
        indexFirstLetter += 1
        stripInput = input[0:indexFirstLetter]
    oneSpace = False # Dumbest possible fix for allowing one space only
    oneDash = False # See above
    extractNum = [] # Extract number from string
    for c in stripInput[::-1]:
        if c == " " and oneSpace == False and c != "- ":
            oneSpace = True
        elif c.isdigit():
            extractNum.append(c)
        elif c == ".":
            extractNum.append(c)
        elif c == "-" and oneDash == False:
            extractNum.append(c)
            oneDash = True
        elif re.search(r"[^\d]|[^.]",c):
            break
    extractNum.reverse()

    foundNum = (''.join(extractNum))

    foundNum = num(foundNum)
    return foundNum,indexFirstLetter
        
# Find matching unit if any, then return index of last letter 
def get_unit_strip(preCutInput, startIndex):
    input = preCutInput[startIndex:startIndex+12] # Use part after number we just split

    # Split at first letter
    index_to_split = re.search(r"\s|[^\w]|$", input).start()
    if index_to_split is not None:
        unit_string = input[0:index_to_split]
        toRemove = unit_string
    else:
        return None
    # Search for shorthand form
    if re.search(r"^(k(m|p)\/?h|mp\/?h|gal|L|lbs|lb|kg|mi|km|cm|in|m|ft|c|f|mm)$", unit_string, re.I):
        if re.search(r"^L$", unit_string, re.I):
            return unit_string.upper(),toRemove
        elif unit_string == "kp/h" or unit_string == "km/h" or unit_string == "mp/h":
            unit_string = unit_string.replace('/','')
            return unit_string.lower(),toRemove
        else:
            return unit_string.lower(),toRemove
    # Search for spelled out form
    elif re.search(r"^(kilometers? per hour|miles? per hour|gallons?|liters?|pounds|kilograms?|miles?|kilometers?|centimeters?|inches|inch|meters?|feet|foot|fahrenheit|celsius|millimeters?)$", unit_string, re.I):
        if re.search(r"^L$", unit_string, re.I):
            return shorten_unit(unit_string).upper(),toRemove
        else:
            unit_string = unit_string.lower()
            # A bunch of special clauses
            # Add s if necessary, so rest of script doesn't break. Very lazy
            if (unit_string == "gallon" or unit_string == "kilogram" or unit_string == "centimeter" or unit_string == "meter" or unit_string == "mile" or unit_string == "centimeter" or unit_string == "liter" or unit_string =="millimeter"):
                unit_string += "s"
            # Special clause for inches
            elif unit_string == "inch":
                unit_string = "inches"
            elif unit_string == "foot":
                unit_string = "feet"
            return shorten_unit(unit_string).lower(),toRemove
    else:
        return None

def get_return_unit(init_unit):
    return return_units.get(init_unit)

def spell_out_unit(unit):
    return spelled_out_units.get(unit)

def shorten_unit(unit):
    for key, value in spelled_out_units.items():
         if unit == value:
             return key

def convert(init_num, init_unit):
    if init_num is None:
        return None

    GAL_TO_L = 3.78541
    LBS_TO_KG = 0.453592
    MI_TO_KM = 1.60934
    IN_TO_CM = 2.54
    FT_TO_M = 0.3048 

    match init_unit:
        case "f":
            return round((init_num - 32) *0.5556 , 2)
        case "c":
            return round((init_num * 1.8) + 32, 2)
        case "gal":
            return round(init_num * GAL_TO_L, 2)
        case "L":
            return round(init_num / GAL_TO_L, 2)
        case ("lbs"|"lb"):
            return round(init_num * LBS_TO_KG, 2)
        case "kg":
            return round(init_num / LBS_TO_KG, 2)
        case ("mi"|"mph"):
            return round(init_num * MI_TO_KM, 2)
        case ("km"|"kph"|"kmh"):
            return round(init_num / MI_TO_KM, 2)
        case "in":
            return round(init_num * IN_TO_CM, 2)
        case "cm":
            return round(init_num / IN_TO_CM, 2)
        case "ft":
            return round(init_num * FT_TO_M, 2)
        case "m":
            return round(init_num / FT_TO_M, 2)
        case "mm":
            return round((init_num / 10) / IN_TO_CM, 4)
        case _:
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
            + " is "
            + str(return_num)
            + " "
            + spell_out_unit(return_unit)
        )

# Handles conversion when provided string
def convertHandler(message, maxResponses):
    results = []
    toConvert = strip_msg(message,maxResponses) # Array of found numbers and units
    for c in toConvert:
        num = c[0]
        unit = c[1]
        returnUnit = get_return_unit(unit)
        convertedNum = convert(num,unit)
        result = get_string(num,unit,convertedNum,returnUnit)
        results.append(result)

    #num = get_num(message) // old safe method
    #unit = get_unit(message) // old safe method

    return results