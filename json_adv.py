
import re

type_dict = {"[": (lambda _: list), "{": (lambda _: dict_checker(_)) , "(": (lambda _: tuple)}

def dict_checker(string):
    sep = "{" if "{" in string else ","
    return dict if ":" in string[:string.find(sep)] else set

reg_datset = re.compile(r"(\(|\[|\{)[^\(\[\{\)\]\}]*(\)|\]|\})")
data_set_global =[]

reg_cheker = re.compile(r"data_set=\|=(\d*)=\|=")

forbidden = ["__import__", "import", "while", "for", "eval", "exec"]


def __string_man(value, int_keys:bool=False):
    """Value moderation"""

    if len(re_lis := list(reg_cheker.finditer(value))) == 1:
        value = loads((data_set_global[int(re_lis[0].group(1))]).group(0), int_keys = int_keys)
    elif len(re_lis) > 1 :
        raise Exception("Do not use two or more iterables inside the same item")
    elif range_obj := re.match(r"range\(\d*,\d*\)", value):
        value = eval(range_obj.group(0))
    elif re.match(r"<.*>", value):
        raise Exception("Use of lambda -- Dont use lambda's at the moment")
    elif value.isnumeric():
        value = int(value)
    elif bool_types := re.match(r"(True|False)", value):
        value = eval(bool_types.group(0))
    else:
        value = value.strip("'") if len(value.strip("'")) != len(value) else value.strip("\"")
    return value


def loads(string:str, int_keys:bool=False, code_blocks:bool=False):
    """ Loading a JSON type string (WITHOUT ESCAPE SEQUENCES) to get corresponding values """

    return_obj = type_dict[string.strip()[0]](string.strip()[1:-1])()
    string = string.strip()[1:-1]

    data_set = list(reg_datset.finditer(string))
    j=0
    while j < len(data_set):
        string = string.replace(data_set[j].group(0), f"data_set=|={len(data_set_global) + j}=|=")
        j += 1
        if j == len(data_set):
            data_set += list(reg_datset.finditer(string))
    data_set_global.extend(data_set)

    if type(return_obj) == dict:
        splist = [i.split(":") for i in string.split(',')]
        for key, value in splist:
            key, value = key.strip(), value.strip()

            if int_keys:
                if key.strip("\"").strip("'").isnumeric():
                    key = eval(key)
                elif key.isnumeric():
                    key = int(key)
            else:
                key = key.strip("'") if len(key.strip("'")) != len(key) else key.strip("\"")

            if (not any(True if i in value  else False for i in forbidden)) and (not code_blocks):
                value = __string_man(value, int_keys)
                return_obj.update({key:value})
            elif code_blocks:
                return_obj.update({key:value})
            else:
                print(value)
                raise Exception("Do not try to use code blocks in values")
    else:
        splist = string.split(",")
        ret_obj = []
        for value in splist:
            value = value.strip()
            if (not any(True if i in value  else False for i in forbidden)) and (not code_blocks):
                value = __string_man(value, int_keys)
                ret_obj.append(value)
            elif code_blocks:
                ret_obj.append(value)
            else:
                print(value)
                raise Exception("Do not try to use code blocks in values")

        return_obj = type(return_obj)(ret_obj)
    return return_obj


def loadf(filename:str, objectname:str, int_keys:bool=False, code_blocks:bool=False):
    """Loading a JSON/Text file to get the data"""
    with open(filename,"r") as file:
        file_val = file.read()

    startposn = file_val.find(f"{objectname} = ") + len(f"{objectname} = ")
    endposn = file_val.find("\n\n", startposn)

    return_obj = loads(file_val[startposn:endposn].replace("\n", "").replace("\t", "").replace("?n?","\n").replace("?t?", "\t"), int_keys, code_blocks)

    return return_obj


def dumps(object, code_blocks:bool=False):
    """ Creating ONE LINE of text for a given object """

    return_str = str(object)
    if any(True if i in return_str  else False for i in forbidden) and (not code_blocks):
        raise Exception("Code Block found in the object")
    else:
        return return_str


def dumpf(object, object_name:str, filename:str, write_type:str="a", code_blocks:bool=False):
    """ Writing an object to a file.. Filename should contain extension too """
    return_str = f"{object_name} = {dumps(object, code_blocks)}"
    return_str = return_str.replace("\n","?n?").replace("\t","?t?")
    quoted = 0
    i = return_str.find("=")+2
    while i < len(return_str):
        if return_str[i] in ["{", "}", ","] and not quoted:
            a = (return_str[:i+1].count("{") - return_str[:i+1].count("}")) + 2
            value = "\n" + ("\t" * a)
            posn = i + 1 - (["{", "}", ","].index(return_str[i])%2)
            return_str = return_str[:posn] + value  +return_str[posn:]
            i += len(value)
        elif return_str[i] == "'":
            quoted = quoted^1
        i +=1 
    return_str += "\n\n"

    with open(filename, write_type) as file:
        file.write(return_str)



if __name__ == '__main__':
    a= {"hello" : "world" , "world" : ["ready",{1,False}, (["why","because"],True)], "c": (lambda : print("k"))}
    print()
    

