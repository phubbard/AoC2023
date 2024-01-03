parts = [
    Part(x=787,m=2655,a=1222,s=2876),
    Part(x=1679,m=44,a=2067,s=496),
    Part(x=2036,m=264,a=79,s=2244),
    Part(x=2461,m=1339,a=466,s=291),
    Part(x=2127,m=1623,a=2188,s=1013),
]

def op_px(part):
    if part.a<2006: return op_qkq(part)
    if part.m>2090: return op_A(part)
    return op_rfg(part)


def split_px(remaining):
    accepted = []
    
    selected, remaining = remaining.space_split('a<2006')
    accepted.append(split_qpq(selected))
    
    selected, remaining = remaining.space_split('m>2090')
    accepted.append(selected)

    selected = remaining
    accepted.append(split_rfg(selected))


def op_pv(part):
    if part.a>1716: return op_R(part)
    return op_A(part)

def op_lnx(part):
    if part.m>1548: return op_A(part)
    return op_A(part)

def op_rfg(part):
    if part.s<537: return op_gd(part)
    if part.x>2440: return op_R(part)
    return op_A(part)

def op_qs(part):
    if part.s>3448: return op_A(part)
    return op_lnx(part)

def op_qkq(part):
    if part.x<1416: return op_A(part)
    return op_crn(part)

def op_crn(part):
    if part.x>2662: return op_A(part)
    return op_R(part)

def op_in(part):
    if part.s<1351: return op_px(part)
    return op_qqz(part)

def op_qqz(part):
    if part.s>2770: return op_qs(part)
    if part.m<1801: return op_hdj(part)
    return op_R(part)

def op_gd(part):
    if part.a>3333: return op_R(part)
    return op_R(part)

def op_hdj(part):
    if part.m>838: return op_A(part)
    return op_pv(part)
