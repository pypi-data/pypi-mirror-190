

def temp_colour(current, min_colour, middle_colour, max_colour):
        colour = min_colour
        if current >= 6:
            colour = max_colour
        elif current >= 2:
            colour = middle_colour
        return colour


# https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range
def rescale(minimum, maximum, current):
    new_min = 1
    new_max = 8
    original_min = minimum
    original_max = maximum
    if current <= original_min:
        return new_min
    elif current >= original_max:
        return new_max
    else:
        return (current - original_min) * (new_max - new_min) / (original_max - original_min) + new_min

