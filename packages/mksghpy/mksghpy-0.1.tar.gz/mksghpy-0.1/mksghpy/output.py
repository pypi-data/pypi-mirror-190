import argparse
import stringsplay as sp

parser = argParser = argparse.ArgumentParser(description= "Pass sring to test")
parser.add_argument('-st', '--string', type= str,required= True,  help = 'i/p string')
args = parser.parse_args()


if __name__ == '__main__':
    fws = sp.Fun_with_strings(args.string)

    print("*"* 100)
    fws.first_three_letters()

    print("*"* 100)
    fws.sequence_letters()

    print("*"* 100)
    fws.unique_letters()