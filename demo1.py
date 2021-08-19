import os

#
# a = "wtf"
# b = "wtf"
# print(a is b)
#
#
# a = "wtf!"
# b = "wtf!"
# print(a is b)
# a, b = "wtf!", "wtf!"
# print(a is b)
funcs = []
results = []
for x in range(7):
    def some_func():
        return x
    funcs.append(some_func)
    results.append(some_func()) # 注意这里函数被执行了

funcs_results = [func() for func in funcs]

