from PIL import Image
import numpy as np
# from RRT import RRT
import matplotlib.pyplot as plt
from matplotlib import cm

kernel_size = 5
sigma = 0.6

def load_map(file_path, resolution_scale):
    ''' Load map from an image and return a 2D binary numpy array
        where 0 represents obstacles and 1 represents free space
    '''
    # Load the image with grayscale
    img = Image.open(file_path).convert('L')
    # Rescale the image
    size_x, size_y = img.size
    new_x, new_y  = int(size_x*resolution_scale), int(size_y*resolution_scale)
    img = img.resize((new_x, new_y), Image.ANTIALIAS)

    map_array = np.asarray(img, dtype='uint8')

    # Get bianry image
    threshold = 127
    # obs=0, free=1
    map_array = 1 * (map_array > threshold)
    # Result 2D numpy array
    return map_array

def gkern(kernel_size, sigma=1, mu=0):
    x, y = np.meshgrid(np.linspace(-1,1,kernel_size), np.linspace(-1,1,kernel_size))
    d = np.sqrt(x*x+y*y)
    return np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )

def grad_map(map_array, risk_points, kernel_size, sigma, max_cost=10):
    grad_map = map_array
    kernel = gkern(kernel_size=kernel_size, sigma=sigma)*max_cost
    kernel_len = len(kernel)
    steps = int(kernel_len/2.2)
    k_flattened = kernel.flatten()
    
    for points in risk_points:
        # Center coordinates
        x, y = points[0], points[1]
        i = 0
        for x_coord in range(x-steps, x+steps+1):
            for y_coord in range(y-steps, y+steps+1):
                grad_map[x_coord][y_coord] = grad_map[x_coord][y_coord]*k_flattened[i]
                i+=1
    return grad_map             
    
if __name__ == "__main__":
    # Load the map
    # start1 = (350-252, 152-100) # Room 1, Inf_RRT_star = 143
    # start2 = (162, 73) # Room 2, Inf_RRT_star = 165
    # start3 = (91, 246) # Room 4, Inf_RRT_star = 111
    # start4 = (184, 321) # Room 5, Inf_RRT_star = 101
    # goal  = (178+26, 275) # Room 3
    # goal  = (135, 151)
    map_array = load_map("/home/aka/capstone_ws/src/autonomous_tb/saved_maps/ground_truth_costmap.pgm", 1)
    #print(map_array)
    risk_coordinates = [(203, 275),(135, 151), (184, 130), (111, 300), (207, 372)]
    gradient_map = grad_map(map_array, risk_coordinates, kernel_size=75, sigma=0.6, max_cost=10)
    gradient_map = np.flipud(gradient_map)
    # print(np.unique(gradient_map))
    
    x_ = 268
    y_ = 111
    print(str(x_) + str(" ") + str(y_))
    print(gradient_map[x_][y_])
    
    # X = np.arange(0,384)
    # Y = np.arange(0,384)
    # X,Y = np.meshgrid(X,Y)
    # fig, ax = plt.subplots(subplot_kw={"projection":"3d"})
    # surf = ax.plot_surface(X,Y,gradient_map,cmap=cm.jet,rstride=1,cstride=1,linewidth=0.,antialiased=False)
    # fig.colorbar(surf,shrink=0.5,aspect=5)

    plt.contour(gradient_map)
    plt.show()

 