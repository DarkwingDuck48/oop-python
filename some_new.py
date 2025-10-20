
def yield_some_object(name):
    print("From yield_some_object")
    yield name
    print("After yield")
    yield f"{name} - good!"

x = yield_some_object("John")
print(f"{next(x)}")

print("===================")

try:
    print(f"{next(x)}")
except StopIteration:
    print("No Values in x")


print(f"{next(x, None)}")

print("1234")