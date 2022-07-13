#Q3
import random
coin = [1, 0]
# 1 means Shir and 0 means Khat


def calculate_expected_value(repetitious_values):
    expected_value = 0
    for item in repetitious_values:
        expected_value += (repetitious_values[item] / 2048) * item
        
        
    print(expected_value)    




def calculate_earned_money(repetitious_values):
    earned_money = 0
    curr_coin = 1
    count = 1
    while curr_coin == 1:
        curr_coin = random.sample(coin, 1)
        curr_coin = curr_coin[0]
        if curr_coin == 1:
            earned_money = 2**count
            count = count + 1
            
    if earned_money not in repetitious_values:
        repetitious_values[earned_money] = 1
    else:
        repetitious_values[earned_money] = repetitious_values[earned_money] + 1   
        
    return repetitious_values        
    
    
repetitious_values = {}    
for i in range(2048):
    repetitious_values = calculate_earned_money(repetitious_values)    
calculate_expected_value(repetitious_values)    