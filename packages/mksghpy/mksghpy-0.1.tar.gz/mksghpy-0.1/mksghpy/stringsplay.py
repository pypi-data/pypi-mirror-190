
class Fun_with_strings():

    """ Test the basic pyton functionality
    Testing the following
    - if.. elif..esle
    - loops - for 
    - Exceptions
    - list comprehension
    -------------------
    Atttributes
    - name or a string
    -------------------
    Methods
    - sequence_letters
    - first_three_letters
    - unique_letters

    """

    def __init__(self, name: str) -> None:
        self.string = name
        pass


    def sequence_letters(self) -> None:
        """ 
        Sequence letter of a string & display letter count
        """
        if not(type(self.string) is str):
            raise Exception('********Please provide string********')
        else:
            # Main stuff
            id = 0
            for letter in self.string:

                # Continue use case
                if letter in [" ", "  ",".","-"]:
                    continue
                
                
                print(f'{id + 1} - {letter}')
                id += 1
            
            print(f"Total letter in string is {id}")


    def first_three_letters(self) -> None:
        """
        Capitalize and print 1st 3 letters
        """
        try:
            # Remove everthing which is not a letter
            for j in [" ", "  ",".","-"]: # could be done better with regex
                self.string = self.string.replace(j, "") 

            # Raise error
            if len(self.string) == 0 :
                print("No letters in string")
                
            else:
                # Main task
                id = 0
                for letter in self.string:
                     # continue use case
                    if letter in [" ", "  ",".","-"]:
                        continue

                    # break use case
                    if id == 3:
                        break

                    print(f'{id + 1} - {letter.capitalize()}')
                    id += 1

        except AttributeError as a:
            print(" -----  Please provide string. Int/Float is provided  -----",a)
        
        except Exception as e:
            print("Something is wrong", e)
        
        else:
            print('No error occured')
        
        finally:
            print("*****HAVE FUN*****")


    def unique_letters(self) -> None:
        """
        Print unique Letters in a string
        """
        # Remove everthing which is not a letter
        for j in [" ", "  ",".","-"]:
            self.string = self.string.replace(j, "") 
        # if_else & list comprehension
        if not(type(self.string) is str):
            raise Exception('********Please provide string********')
        else:
            # list comprehension & Set
            items = sorted(set( [g.lower() for g in self.string]))
            [print(f'{k[0]} - {k[1]}') for k in enumerate(items)]

        
# l = Fun_with_strings("manik")
# l.first_three_letters()


# class Basic_py:
#     """ Test the basic pyton functionality

#     -------------------
#     Atttributes
#     - user_initial

#     -------------------
#     Methods
#     - get_user
#     - set_user

#     """
#     def __init__(self,user_initial) -> None:

#         """ Necessry attributes for the Basic_py object
#         ----------------------------------------
#         Parameters:
#         name : str 
#             user credential who is running the test
#         """

#         self.user = user_initial
#         pass
    
#     def get_user():
#         """get the user name"""
#         return self.user

#     def set_user(self, name):
#         """set user name"""
#         self.user = name








