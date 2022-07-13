#Q2
import random
import matplotlib.pyplot as plt

def f_function(x):
    return (1 - (x**2))**(1/2)

def show_chart(n_with_values):
    left = [1, 2, 3, 4, 5, 6]
  
    height = []
    for i in range(len(n_with_values)):
        height.append(n_with_values[i][1])
        height.append(n_with_values[i][2])

    tick_label = ['E[X]', 'Var', 'E[X]', 'Var', 'E[X]', 'Var']

    plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['red', 'red', 'blue', 'blue', 'green', 'green']  )

    plt.xlabel('X')
    plt.ylabel('E[x] and Var')
    plt.title('My chart with n=100, n=1000 and n=10000')
    plt.show()

def calculate_expection_value(n):
    sample_list = []

    f_list = []

    for i in range(n):
        sample_list.append(random.uniform(0, 1))
        f_list.append(f_function(sample_list[i]))
    
    
    expection_value = 0 
    for i in range(n):
        expection_value += f_list[i]
    expection_value /= n
        
    var = 0
    for i in range(n):
        var += (f_list[i] - expection_value)**2
    var /= n


    return expection_value, var

n_with_values = []
n = 100
expection_value, var = calculate_expection_value(n)
print("for   n = " + str(n) + " for first time,    E = " + str(expection_value) + "   Var = " + str(var))
n_with_values.append([n, expection_value, var])

n = 100
expection_value, var = calculate_expection_value(n)
print("for  n = " + str(n) + " for second time,    E = " + str(expection_value) + "   Var = " + str(var))



n = 1000
expection_value, var = calculate_expection_value(n)
print("for  n = " + str(n) + " for first time,    E = " + str(expection_value) + "   Var = " + str(var))
n_with_values.append([n, expection_value, var])


n = 10000
expection_value, var = calculate_expection_value(n)
print("for n = " + str(n) + " for first time,    E = " + str(expection_value) + "   Var = " + str(var) + "\n")
n_with_values.append([n, expection_value, var])


show_chart(n_with_values)