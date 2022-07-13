#ًQ1
import random
import matplotlib.pyplot as plt


def show_chart(three_ways_probability, n):
    left = [1, 2, 3]
  
    height = three_ways_probability

    tick_label = ['first way', 'second way', 'thrid way']

    plt.bar(left, height, tick_label = tick_label,
        width = 0.8, color = ['red', 'green', 'blue'])

    plt.xlabel('ways')
    plt.ylabel('probability')
    plt.title('My chart with n=' + str(n))
    plt.show()

def first_way(first_chosen):
    if first_chosen == 1:
        return 1
    else:
        return 0
    
def second_way(first_chosen):
    if first_chosen == 1:
        return 0
    else:
        return 1    
    
    
def third_way(prizes, first_chosen):
    probability_50_percent = [0 ,1]
    is_change = random.sample(probability_50_percent, 1)
    if is_change[0] == 0:
        if first_chosen == 1:
            return 1
        else:
            return 0
        
    else:
        if first_chosen == 1:
            return 0
        else:
            return 1

def calculate_three_ways(n):
    three_ways_probability = []
    wins_num=0
    for i in range(n):
        #define goat as 0 and car as 1
        prizes = [0, 0, 1]
        first_chosen = random.sample(prizes, 1)
        prizes.remove(*first_chosen)
        wins_num = wins_num + first_way(*first_chosen)
        
    three_ways_probability.append(wins_num/n)        
        
    wins_num=0
    for i in range(n):
        #define goat as 0 and car as 1
        prizes = [0, 0, 1]
        first_chosen = random.sample(prizes, 1)
        prizes.remove(*first_chosen)
        wins_num = wins_num + second_way(*first_chosen)

    three_ways_probability.append(wins_num/n) 

    wins_num=0
    for i in range(n):
        #define goat as 0 and car as 1
        prizes = [0, 0, 1]
        first_chosen = random.sample(prizes, 1)
        prizes.remove(*first_chosen)
        wins_num = wins_num + third_way(prizes, *first_chosen)   
        
    three_ways_probability.append(wins_num/n) 
        
    show_chart(three_ways_probability, n)    

        
        
calculate_three_ways(10)
calculate_three_ways(100)
calculate_three_ways(1000)
calculate_three_ways(10000)