def greet(func):
    def mod_fuc(*args, **kwargs):
        print("Good Morning")
        func(*args, **kwargs)
        #we can add post steps also
    return mod_fuc

@greet
def add(num1,num2):
    print("We will do addition")
    print(num1+num2)

add(1,2)