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


# calculate the approximate absolute relative error between the root from a root finding iteration
def calculate_absolute_relative_error(new_root: Decimal, old_root: Decimal):
    return (
        (new_root - old_root).copy_abs() / new_root.copy_abs()
        if new_root != 0
        else (new_root - old_root).copy_abs()
    )


# calculate the number of correct significant figures from absolute relative error
# dervied from the formula: e_s ≈ 0.5 * 10^(2 - n)
def calculate_number_of_correct_significant_figures(
    absolute_relative_error: Decimal, precision: int
) -> int:
    if absolute_relative_error > 0:
        m = Decimal("2") - (Decimal("200") * absolute_relative_error).log10()
        return max(0, int(m))
    else:
        return precision
