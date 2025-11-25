from decimal import Decimal


def remove_trailing_zeros(value: Decimal) -> Decimal:
    value = value.normalize()
    if value == value.to_integral_value():
        return value.to_integral_value()
    return value
