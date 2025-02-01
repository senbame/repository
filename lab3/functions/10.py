def unique_list():
    lst = map(int, input().split())
    lst = list(lst)
    null_lst = []
    for i in lst:
        if i not in null_lst:
            null_lst.append(i)
    print(sorted(null_lst))
unique_list()
