import ast


dict = {1:2, 3:4}
print('dict:', dict)
print('type of dict', type(dict))

str = '{1:2, 3:4}'
print('str:', str)
print('type of str', type(str))

dict1 = (ast.literal_eval(str))
print(dict1[1])