# Yvnee / Eirav @ GitHub — 30.10.2023

global STRUCT

STRUCT = dict()
DEBUG = False

KEYNAMES = ["u", "r", "i", "p"]


class Struct(): # Root structure of build  ————————————————————————————————————————————————————————————————

    # Create new STRUCT function —————————————————————————————————————————————————————————————————————

    def override(**newdata):
        global STRUCT
        if STRUCT is dict:
            STRUCT.clear()
        else:
            STRUCT = {}
    

        for name in KEYNAMES: STRUCT[name]={"equation": None, "numbers": None, "result": None}

    # STRUCT update function ————————————————————————————————————————————————————————————————————————

    def update(parent, edit):
        global STRUCT
        STRUCT[parent]["equation"] = edit[0]
        STRUCT[parent]["numbers"] = edit[1]
        STRUCT[parent]["result"] = edit[2]
    
    # Clean function ——————————————————————————————————————————————————————————————————————————————
    
    def clean_number(number = int):
        try:
            # Creating these variables to get decimals, there are other ways, yes.
            if (float(number) - int(number)) > 0.001:
                return '%.3f' % round(number, 2)
            else:
                raise ValueError(f"Number {number} does not have decimals strong enough to even out")
        except (TypeError, ValueError):
            value = number

            try: value = int(number) 
            except TypeError: pass
            return value

    # Settle function —————————————————————————————————————————————————————————————————————————————

    def settle_ohm_variables(req = str):
        req = req.lower()
        string = (req == "u" and "V" or req == "r" and "Ω" or req == "i" and "A" or req == "p" and "W") or "x"
        return string

     # Mending function —————————————————————————————————————————————————————————————————————————————

    def mend(string="Example: U / R = I", numberlist=[1, 2, 3]):
        product = string
        for string_key in string:
            if string_key in KEYNAMES:
                if len(numberlist) < 1:
                    return product

                product = product.replace("^2", "", -1).replace(string_key, str(Struct.clean_number(numberlist[0])) + " " + Struct.settle_ohm_variables(string_key), 2)
                numberlist.remove(numberlist[0])
        return product

    # Met function ————————————————————————————————————————————————————————————————————————————————

    def met(parent, child, dict_value):
        if parent is list: parent.append(child)
        elif parent is dict: parent[child] = dict_value
        return parent
    
    # Flush function ——————————————————————————————————————————————————————————————————————————————

    def flush(parent):
        if parent is list: parent = list()
        elif parent is dict: parent = dict()
        return parent
    
    # Formate STRUCT function ——————————————————————————————————————————————————————————————————————————————
    
    @staticmethod

    def form(**data):
        product = str()

        for variable, value in STRUCT.items():
            if value['result']:
                mend_equation = Struct.mend(value['equation'], value['numbers'])

                product = product + f"{variable.upper()} = {value['equation']} = {mend_equation} = {Struct.clean_number(value['result'])} {Struct.settle_ohm_variables(variable.upper())}\n"
            else:
                Logic.execute(u=STRUCT['u']['result'], r=STRUCT['r']['result'], i=STRUCT['i']['result'], p=STRUCT['p']['result'])
                return Struct.form(u=STRUCT['u']['result'], r=STRUCT['r']['result'], i=STRUCT['i']['result'], p=STRUCT['p']['result'])
        return product

    # Finalize function (Set missing values) ———————————————————————————————————————————————————————
   
    @staticmethod 
    
    def finalize():
        global STRUCT
        if STRUCT is dict:
            for name, value in STRUCT.items():
                FUNCTION = getattr(Logic, name.lower())
                if STRUCT[name]["result"] is None:
                    FUNCTION(STRUCT["u"]["result"], STRUCT["r"]["result"], STRUCT["i"]["result"], STRUCT["p"]["result"])
        return STRUCT
    
    # ——›—— END OF STRUCT CLASS ——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——

class Logic(): # All mathematical logic  —————————————————————————————————————————————————————————————————————————————————————

    # Voltage logic ——————————————————————————————————————————————————————————————————————————————————————————————————————————

    def u(data):
        u, r, i, p = (data['u'], data['r'], data['i'], data['p'])
        if u is not None:
            return Warning(f"Merit @ u = {u}")
        usage_type = "u"
        if r and i: Struct.update(usage_type, ["r * i", [r, i], r * i])
        elif p and r: Struct.update(usage_type, ["√(p * r)", [p, r], (p * r) ** (1 / 2)])
        elif p and i: Struct.update(usage_type, ["p / i", [p, i], p / i])
    
    # Resistance logic ———————————————————————————————————————————————————————————————————————————————————————————————————————

    def r(data):
        u, r, i, p = (data['u'], data['r'], data['i'], data['p'])
        if r is not None:
            return Warning(f"Merit @ r = {r}")
        usage_type = "r"
        if u and i: Struct.update(usage_type, ["u / i", [u, i], u / i])
        elif u and p: Struct.update(usage_type, ["u^2 / p", [u, p], u * u / p])
        elif p and i: Struct.update(usage_type, ["p / i^2", [p, i], p / i * i])
    
    # Ampere logic ———————————————————————————————————————————————————————————————————————————————————————————————————————————

    def i(data):
        u, r, i, p = (data['u'], data['r'], data['i'], data['p'])
        if i is not None:
            return Warning(f"Merit @ i = {i}")
        usage_type = "i"
        if u and r: Struct.update(usage_type, ["u / r", [u, r], u / r])
        elif p and u: Struct.update(usage_type, ["p / u", [p, u], p / u])
        elif p and r: Struct.update(usage_type, ["√P / r", [p, r], p ** (1 / 2) / r])
    
    # Watt logic ————————————————————————————————————————————————————————————————————————————————————————————————————————————

    def p(data):
        u, r, i, p = (data['u'], data['r'], data['i'], data['p'])
        if p is not None:
            return Warning(f"Merit @ p = {p}")
        usage_type = "p"
        if u and i: Struct.update(usage_type, ["u * i", [u, i], u * i])
        elif r and i: Struct.update(usage_type, ["r * i^2", [r, i], r / i * i])
        elif u and r: Struct.update(usage_type, ["u^2 / r", [u, r], u * u / r])
    
    def simplify(structure = dict):
        try:
            product = dict()
            for key_name, key_product in structure.items():
                product[key_name.lower()] = key_product['result']
            return product
        except (TypeError, ValueError, AttributeError):
            return Warning(f"Requested structure is not a valid dictionary. Have you used a proper root for your structure?\nYour provided structure: {structure}")

    def execute(**data):
        for key, val, in STRUCT.items():
            if key in KEYNAMES and val['result'] is None:
                FUNCTION = getattr(Logic, key.lower())
                FUNCTION(data)
                DEBUG: print(f"Ran function {key.lower()}({data})")
        return Struct.finalize()

    # ——›—— END OF LOGIC CLASS ——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——›——


# ACCESSIBLE FUNCTIONS ———————————————————————————————————————————————

# Solve connection ∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙
def solve(volt=None, resistance=None, ampere=None, watt=None, formation=False, discipline=False):
    if not discipline: Struct.override()
    EXECUTION = Logic.execute(u=volt, r=resistance, i=ampere, p=watt)
    if formation: return Struct.form(u=volt, r=resistance, i=ampere, p=watt)
    else: return EXECUTION

# Mend connection ∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›∙›
def mend(string=str(), numberlist=list()):
    return Struct.mend(string, numberlist)