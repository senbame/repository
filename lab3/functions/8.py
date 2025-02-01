def spy_game(nums):
    string = ""
    for i in nums:
        if i == 0:
            string += str(i)
        if i == 7:
            string += str(i)
    if "007" in string:
        return True
    return False
spy = ([1,0,2,4,0,5,7]) 
print(spy_game(spy))
         
        