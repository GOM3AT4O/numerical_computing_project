from decimal import Decimal


def remove_trailing_zeros(value: Decimal) -> Decimal:
    if value == 0:
        value = Decimal(0)
    return (
        value.to_integral_value()
        if value == value.to_integral_value()
        else value.normalize()
    )
