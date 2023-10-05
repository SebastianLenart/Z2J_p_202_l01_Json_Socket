import json

json1 = {
    "user": None,
    "command": None,
    "password": None
}


# print(json1)
# print(type(json1))
#
# json2 = json.dumps(json.dumps(json1))
#
# print(json2)
# print(type(json2))
#
# json3 = json.loads(json2)
# print(json3)
# print(type(json3))

def forwared_args(ar1, ar2):
    print(ar1)
    print(ar2)

a, *b = ["1", "2", "3", "4"]
print(a)
print(type(b), "".join(list(map(lambda x: x+" ", b))))
