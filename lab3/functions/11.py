def palindrome():
    string = input()
    if string == string[::-1]:
        return True
    return False
print(palindrome())