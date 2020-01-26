# Flattens an array of arbitrarily nested arrays of integers

array_of_arbitrarily_nested_arrays_of_ints = [345, 2342, [76456, 323, 23478, 2], 7634, 7345, 234, [345, 788, 234, 956], 23423467, 4357]

flattened_array_of_ints = []

for index in array_of_arbitrarily_nested_arrays_of_ints:
    if type(index) is int:
        flattened_array.append(index)
    elif type(index) is list:
        flattened_array_of_ints += index
