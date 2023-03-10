with open('game.txt', 'r') as file:
    lines = [line.rstrip() for line in file]

Vars = []


class Variable:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def set_var(self, value):
        self.value = value


def get_calculation(string):
    try:
        # Split the input string into tokens separated by spaces
        tokens = string.split()

        # Replace any variable tokens with their corresponding values
        for var in Vars:
            for i in range(len(tokens)):
                if tokens[i].isalpha() and tokens[i] != "True" and tokens[i] != "False":
                    # If the token is a variable name, check if it's a string or numeric variable
                    is_string = False
                    for char in tokens[i]:
                        if char == '"':
                            is_string = not is_string
                    if not is_string:
                        # If it's a numeric variable, replace it with its value
                        if tokens[i] == var.name:
                            tokens[i] = str(var.value)
                    else:
                        # If it's a string variable, remove the quotes
                        if tokens[i] == f'"{var.name}"':
                            tokens[i] = var.value

                elif tokens[i].isnumeric():
                    tokens[i] = str(tokens[i])

        # Join the tokens back into a single string
        expr = " ".join(tokens)

        # Evaluate the expression and return the result
        result = eval(expr)

        return str(result)
    except:
        return None


def run_line(string):
    if string.startswith("print"):
        result = get_calculation(string[5:])
        print(result)

    if string.startswith("var"):
        s = string[3:]
        tokens = s.split()

        variable_name = None
        operator = None
        variable_value = ""

        for i, token in enumerate(tokens):
            if i == 0:
                variable_name = token
            elif token in ["+=", "-=", "*=", "/=", "="]:
                operator = token
            else:
                variable_value += " " + token

        # Check if the variable name is already in the list of Variables
        found_var = False
        for var in Vars:
            if var.name == variable_name:
                found_var = True
                break

        # If the variable is not already in the list, create a new Variable object and add it to the list
        if not found_var:
            new_var = Variable(variable_value.strip(), variable_name)
            Vars.append(new_var)

        # If the variable is already in the list, update its value
        else:
            for var in Vars:
                if var.name == variable_name:
                    calculation_result = get_calculation(variable_value.strip())
                    if calculation_result is None:
                        break
                    if operator == "=":
                        var.set_var(calculation_result)
                    elif operator == "+=":
                        var.set_var(var.value + calculation_result)
                    elif operator == "-=":
                        var.set_var(var.value - calculation_result)
                    elif operator == "*=":
                        var.set_var(var.value * calculation_result)
                    elif operator == "/=":
                        var.set_var(var.value / calculation_result)


for i in range(len(lines)):
    run_line(lines[i])
