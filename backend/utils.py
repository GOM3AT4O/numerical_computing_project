from decimal import Decimal


# remove trailing zeros and unnecessary exponent from a Decimal value
# for better readability in the output
def remove_trailing_zeros(value: Decimal) -> Decimal:
    if value == 0:
        value = Decimal(0)
    return (
        value.to_integral_value()
        if value == value.to_integral_value()
        else value.normalize()
    )
