class bcolors:
    HEADER = '\033[1;98m'
    OKBLUE = '\033[1;34m'
    OKCYAN = '\033[1;96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

x = "lol"


print(f"{bcolors.HEADER}HEADER: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.OKBLUE}OKBLUE: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.OKGREEN}OKGREEN: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.WARNING}Warning: No active frommets remain. Continue?{bcolors.ENDC}" + "test: %s" %x)
print(f"{bcolors.FAIL}FAIL: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.BOLD}BOLD: No active frommets remain. Continue?{bcolors.ENDC}" + x)
print(f"{bcolors.UNDERLINE}UNDERLINE: No active frommets remain. Continue?{bcolors.ENDC}" + x)


