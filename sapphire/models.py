import sapphire.model.zero

def zero(prompt):
    model = sapphire.model.zero.SapphireZero(prompt)
    return model.output()