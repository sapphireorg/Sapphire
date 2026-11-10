import sapphire.model.zero

def zero(prompt, environment):
    model = sapphire.model.zero.SapphireZero(prompt, environment)
    output = ""

    for i in model.output(): output += i + " "
    
    return output