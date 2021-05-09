filepath = 'enums_to_create_example.txt'

arr = [] 
with open(filepath) as fp:
   line = fp.readline()
   cnt = 1
   while line:
       arr.append(line.strip())
    #    print("Line {}: {}".format(cnt, ))
       line = fp.readline()
       cnt += 1


       
print(arr)


