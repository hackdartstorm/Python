# 1.
def check_value(input_value):
    match input_value:
        case 1:
            return "tapped 1"
        case 404:
            return "404 error"
        case 99:
            return "99"
        case _:
            return "aagye line me"


print(check_value(int(input("Enter between this [1 or 404 or 99] : "))))


# 2.
def get_http_status(status_code):
    match status_code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:
            return "Unknown status"


print(get_http_status(5007))
