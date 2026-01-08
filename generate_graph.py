num_rows = 17
max_in_row = 5
start_x = 500
start_y = 100
gap_x = 100
gap_y = 50

print('{"nodes": [')

id = 0
previous_was_max = False
for row in range(num_rows):
    
    num_in_row = min(row + 1, num_rows - row)    #max_in_row
    
    if (num_in_row >= max_in_row):
        if previous_was_max:
            num_in_row = max_in_row - 1
            previous_was_max = False
        else:
            num_in_row = max_in_row
            previous_was_max = True

    for node in range(num_in_row):
        #start_x = 200
        #if row % 2:
        #    start_x = 100
        #print('{' + f'"id":{id}, "x":{start_x+node*(gap_x*2)}, "fy":{start_y+gap_y*row}' + '},')
        x = "x"
        y = "y"
        if (node == 0) or (node == num_in_row-1):
            x = "fx"
            y = "fy"
        print('{' + f'"id":{id}, "{x}":{int(start_x+(node-((num_in_row-1)/2))*(gap_x*2))}, "{y}":{start_y+gap_y*row}' + '},')
        id += 1

print(']')


for i in range(id):
    neighbors = []

    if i >= 2*num_in_row:
        neighbors.append(i-2*num_in_row)
    if i >= num_in_row:
        neighbors.append(i-num_in_row)

        #if i % num_in_row != 0: #left wall
        #    neighbors.append(i-num_in_row-1)
        if (i-num_in_row-1) % num_in_row != 0:  #right wall
            neighbors.append(i-(num_in_row-1))
        #    neighbors.append(i-num_in_row)
    if i < (num_rows-2)*num_in_row:
        neighbors.append(i+2*num_in_row)
    if i < (num_rows-1)*num_in_row:
        if i % num_in_row != 0: #left wall
            neighbors.append(i+num_in_row-1)
        if (i-num_in_row-1) % num_in_row != 0:  #right wall
            neighbors.append(i+num_in_row)
    
    print(i, sorted(neighbors))
    



    #if i % (2*max_in_row-1) == 0:
    #    print(i, "outer left")
    #elif (i - max_in_row) % (2*max_in_row-1) == 0:
    #    print(i, "inner left")
    #elif i - (max_in_row-1) % (2*max_in_row-1) == 0:
    #    print(i, "outer right")
    #elif (i - ((2*max_in_row-1)-1)) % (2*max_in_row-1) == 0:
    #    print(i, "inner right")