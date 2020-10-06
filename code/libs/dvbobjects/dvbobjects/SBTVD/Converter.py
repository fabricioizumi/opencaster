def convert_to_bcd(numero):
    if (numero < 0  or numero > 99):
        return 0

    upper_digit = int(numero/10)

    lower_digit = numero - (upper_digit * 10)

    return lower_digit + (upper_digit * 16)


