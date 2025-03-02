def palindrome(s):
    return s == s[::-1]
s = "KAZAK"
print(palindrome(s))