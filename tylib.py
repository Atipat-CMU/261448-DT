def is_type(list, desired_type):
    return all(isinstance(element, desired_type) for element in list)
