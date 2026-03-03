# 1.
def check_val(val):
    match val:
        case 1:
            return "tapped 1"
        case 404:
            return "404 error"
        case 99:
            return "99"
        case _:
            return "aagye line me"


print(check_val(int(input("Enter between this [1 or 404 or 99] : "))))


# 2.
def http_status(status): 
    match status:  
        case 200: 
            return "OK" 
        case 404: 
            return "Not Found" 
        case 500: 
            return "Internal Server Error" 
        case _: 
            return "Unknown status"  


print(http_status(5007))
