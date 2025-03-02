import time
import math
def invoke(n , ml):
    time.sleep(ml / 1000)
    result = math.sqrt(n)
    print(f"Square root of {n} after {ml} miliseconds is {result}")
number = int(input())
t = int(input())
invoke(number , t)