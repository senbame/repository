def solve(numheads , numlegs):
    x = numheads - ((4*numheads - numlegs) / 2)
    y = (4*numheads - numlegs) / 2
    print("Number of chickens: " , x)
    print("Number of rabbiis: ", y)
heads = 35
legs = 94
solve(heads , legs)