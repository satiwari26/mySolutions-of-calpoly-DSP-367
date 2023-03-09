from my_fifo import my_fifo

fifo = my_fifo(3)
x= [0]
for i in range(len(x)-1,len(x)+10):
    x.append(i)

print(x[0])
print(x[1])
print(x[2])
print(x[3])