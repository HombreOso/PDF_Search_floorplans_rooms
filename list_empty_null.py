# show that empty list and None vales are evaluated as False in if statements

list_empty = []

list_non_empty = [1, 2]

null_value = None

if null_value:
    print("Null value true")
else:
    print("Null value false")

if list_empty:
    print("list_empty true")
else:
    print("list_empty false")

if list_non_empty:
    print("list_non_empty true")
else:
    print("list_non_empty false")#
