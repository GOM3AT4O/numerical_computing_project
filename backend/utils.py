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


def calculating_number_of_correct_significant_figures(
    es: Decimal, precision: int
) -> int:
    if es > 0:
        m = Decimal("2") - (Decimal("2") * es).log10()
        return max(0, int(m))
    else:
        return precision
