
import os
# import Bulk_fix_KR_LN_lines_formats
# from Obsolete_Version import Bulk_fix_OtomegeKR_V4Formatting
# import tester
# from Bulk_fix_KR_LN_lines_formats import convert_to_standard_quote

class bcolors:
    HEADER = '\033[1;98m'
    OKBLUE = '\033[1;34m'
    OKCYAN = '\033[1;96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("@tester2")

x = "lol"


print(f"{bcolors.HEADER}HEADER: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.OKBLUE}OKBLUE: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.OKCYAN}OKGREEN: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.ENDC}" + "test: %s" %x)
print(f"{bcolors.FAIL}FAIL: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.BOLD}BOLD: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.UNDERLINE}UNDERLINE: No active frommets remain. Continue?{bcolors.ENDC}" + x)


def mF():
    local_v = 6

    def definnerF():
        nonlocal local_v
        print("@definnerF %i"  %local_v)
        local_v = 12

    definnerF()
    print(local_v)

mF()


def mF2():
    local_v = 8
    def definnerF(y):
        print("@definnerF %i" %y)
        y = 13

    definnerF(local_v)
    print(local_v)

mF()


print(os.getcwd())
