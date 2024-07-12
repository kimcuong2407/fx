def do_stuff_with_number(n):
    print(n)

def catch_this():
    the_list = (1,2)

    for i in range(3):
        try:
            print('try')
            do_stuff_with_number(the_list[i])
        except IndexError as error:
            print( error) # An error occurred: name 'x' is not defined
            do_stuff_with_number('errror')
        
catch_this()