import sapphire.model.zero

def zero(prompt):
    model = sapphire.model.zero.SapphireZero(prompt)
    output = ""

    for i in model.output(): output += i + " "
    
    return output