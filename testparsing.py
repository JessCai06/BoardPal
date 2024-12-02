def parse_points_and_order(input_string):
    # Find the start and end indices for the "points" and "order" sections
    points_start = input_string.find('"points": [') + len('"points": [')
    points_end = input_string.find(']', points_start)
    
    order_start = input_string.find('"order": [') + len('"order": [')
    order_end = input_string.find(']', order_start)
    
    # Extract the substrings containing the points and order
    points_str = input_string[points_start:points_end]
    order_str = input_string[order_start:order_end]
    
    # Parse points: Split by "), (" and remove the surrounding parentheses and extra spaces
    points = []
    points_list = points_str.split('), (')
    for point in points_list:
        # Remove any surrounding spaces and parentheses, then convert to a tuple of floats
        point = point.strip(' ()')
        point_tuple = tuple(map(float, point.split(',')))
        points.append(point_tuple)
    
    # Parse order: Split by '], [' and convert to lists of integers
    order = []
    order_list = order_str.split('], [')
    for group in order_list:
        # Remove any surrounding spaces and brackets, then split by commas and convert to integers
        group = group.strip(' []')
        group_list = list(map(int, group.split(',')))
        order.append(group_list)
    
    return points, order

# Example usage:
input_string = '''"points": [(1, 0, 0), (0.7071, 0.7071, 0), (0, 1, 0), (-0.7071, 0.7071, 0), (-1, 0, 0), (-0.7071, -0.7071, 0), (0, -1, 0), (0.7071, -0.7071, 0), (1, 0, 1), (0.7071, 0.7071, 1), (0, 1, 1), (-0.7071, 0.7071, 1), (-1, 0, 1), (-0.7071, -0.7071, 1), (0, -1, 1), (0.7071, -0.7071, 1)], "order": [[0, 1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14, 15], [0, 1, 9, 8], [1, 2, 10, 9], [2, 3, 11, 10], [3, 4, 12, 11], [4, 5, 13, 12], [5, 6, 14, 13], [6, 7, 15, 14], [7, 0, 8, 15]]'''

points, order = parse_points_and_order(input_string)
print("Points:", points)
print("Order:", order)
