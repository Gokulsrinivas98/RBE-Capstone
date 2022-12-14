import numpy as np

list = np.array([[0,1,0,0],
                 [0,0,0,1],
                 [0,0,0,0]])

num = np.where(list == 1)
print(num)

# my_list = ['A', 'B', 'C', 'D', 'E', 'F']
# print("The index of element C is ", my_list.index('C'))
# print("The index of element F is ", my_list.index('F'))