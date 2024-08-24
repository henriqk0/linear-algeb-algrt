import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, math

def clear_terminal():
    return os.system('clear') if (os.name == 'posix') else os.system('cls')


# function to calculate the bernstein polynomial
def bernstein_poly(i, n, t):
    return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i)) # numpy broadcasting (operations (as **i and -1) are applied element by element of the array)


# function to calculate the Bézier curve
def bezier_curve(t, points):
    n = len(points) - 1                     # degree according to the number of points
    curve = np.zeros((len(t), 2))             # 100x2 (2D) matrix with only 0
    for i in range(len(points)):                # the somatory
        b_p = bernstein_poly(i, n, t)
        curve += np.outer(b_p, points[i])     # outer -> multpl.
    return curve


# function to calculate the Bézier Biocubic Surface
def bicubic_bezier_surface(u, v, control_points):
    n = 3  # cubic degree
    surface_point = np.zeros(3)
    for i in range(4):
        for j in range(4):
            bernstein_u = bernstein_poly(i, n, u)
            bernstein_v = bernstein_poly(j, n, v)
            surface_point += bernstein_u * bernstein_v * control_points[i, j]
    return surface_point


def surfc_gen():
    print("Generating the surface with Bézier bicubic")
    control_points = np.zeros((4, 4, 3)) # 4x4 - requirement to bezier surfc.
    # 4x4 matrix (3 = [x,y,z] as elements)
    
    # User inputs
    for i in range(4):
        for j in range(4):
            x = float(input(f"x coord. of control point ({i+1}, {j+1}): "))
            y = float(input(f"y coord. of control point ({i+1}, {j+1}): "))
            z = float(input(f"z coord. of control point ({i+1}, {j+1}): "))
            control_points[i, j] = [x, y, z]    # control_pointss[i, j] == ''[i][j]
    
    # u and v paramethers to the surface (like t in curves)
    u_values = np.linspace(0, 1, 30)
    v_values = np.linspace(0, 1, 30)
    
    # gen. points (bezier alg. for surfaces) (list comprehension w/ numpy array)
    surface_points = np.array([[bicubic_bezier_surface(u, v, control_points) for v in v_values] for u in u_values])
    
    # Separating the x, y, z (turn most legible)
    X = surface_points[:, :, 0]
    Y = surface_points[:, :, 1]
    Z = surface_points[:, :, 2]
    # ploting, descriptions, show
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') # Axes3D (2 argument), 1 1 1 = number of rows, of columns and subplot index (1 to first subplot, 2 to next, ...)  
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_title("Bicubic Bézier Surface")
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    plt.show()
    input("Press any key to continue . . .")
    clear_terminal()


def curv_gen():
    print("Generating the curve with Bézier equation")
    
    while True:
        num_test = input("Number of points: ")
        try:
            num_points = int(num_test)
            if num_points > 0:
                break
            else:
                print(f"Invalid number of points ({num_test}).")
        except ValueError:
            print("Only numbers allowed.")

    points = []

    for i in range(num_points):
        x = float(input(f"x coord. of point {i+1}: "))
        y = float(input(f"y coord. of point {i+1}: "))
        points.append([x, y])

    points = np.array(points)

    t = np.linspace(0, 1, 100)  # array of 100 elements from 0 to 1 equally spaced

    curve = bezier_curve(t, points)

    plt.plot(curve[:, 0], curve[:, 1], label='Bézier curve')            #(all) (xi, yi)
    plt.plot(points[:, 0], points[:, 1], 'ro-', label='Control points') #(all) (xi, yi)
    plt.title("Bézier curve")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.legend()
    plt.show()
    input("Press any key to continue . . .")
    clear_terminal()

def main():
    msg = """
    Type _ to:
    [1] : Generate curves
    [2] : Generate Surfaces
    [3] : Quit
    """
    option = input(msg)
    while (option != '3'):
        clear_terminal()
        if (option == '1'):
            curv_gen()
        elif (option == '2'):
            surfc_gen()

        if option not in ['1', '2'] and option != '3':
            print("Please enter a valid input.")
            print()


        option = input(msg)

if __name__ == "__main__":
    main()