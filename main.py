import numpy as np
import math
import scipy 

class BoxGame:
    
    def __init__(self) -> None:
        self.nums_left = list(np.arange(1, 13))
        self.roll = -1
        self.game_alive = True
    
    def make_selection(self):
        valid = False
        while not valid:
            valid = True
            in_string = input("Select numbers: ")
            nums = in_string.split(",")
            nums = [int(num) for num in nums]
            
            if sum(nums) != self.roll:
                print("Numbers must add to your roll total.")
                valid = False
            
            else:
                for num in nums:
                    if num not in self.nums_left:
                        print(f"{num} has already been played.")
                        valid = False
        return nums
    
    def check_if_moves_left(self, nums_left=None, running_sum=0):
        if nums_left is None:
            nums_left = self.nums_left.copy()
        if running_sum == self.roll:
            return True
        if len(nums_left) == 0:
            return False
        if running_sum > self.roll:
            return False
        
        for i in range(len(nums_left)):
            num = nums_left.pop(i)
            if self.check_if_moves_left(nums_left, running_sum + num):
                return True
            
            if self.check_if_moves_left(nums_left, running_sum):
                return True
            
            nums_left.insert(i, num)
            if running_sum + nums_left[0] > self.roll:
                break
            
        return False  
    
    def take_turn(self):
        print(f"\nYour numbers: {self.nums_left}")
        self.roll = np.random.randint(1, 7) + np.random.randint(1, 7)
        print(f"You rolled: {self.roll}")
        
        if not self.check_if_moves_left():
            print("No available moves. Game over.")
            self.game_alive = False
            return
        
        selections = self.make_selection()
        
        for selection in selections:
            self.nums_left.remove(selection)
    
    def game_loop(self):
        while self.game_alive:
            self.take_turn()

class Trainer():
    
    def __init__(self) -> None:
        self.gama = 0.9
        self.state_space = []
        self.action_space = []
        self.transition_function = self.transition_function
        self.reward_function = self.reward_function_simple
    
    def U(self, s):
        return 0
    
    def lookahead(self, U, s, a):
        val = self.reward_function(s, a)
        val += self.gama * sum([self.transition_function(sp, s, a) * self.U(sp) for sp in self.state_space])
        return val
    
    def allowed(self, a, s_nums, roll):
        if sum(a) != roll:
            return False
        for move in a:
            if move not in s_nums:
                return False
        
        return True
        
    def transition_function(self, sp, s, a):
        s_nums, roll = s
        s_nums_p, roll_p = sp
        if not self.allowed(a, s_nums, roll):
            return 0
        
        if s_nums != [num for num in s_nums_p if num not in a]:
            return 0
        
        return self.two_dice_dist(roll_p)
    
    def reward_function_simple(self, s, a):
        s_nums, roll = s
        if not self.allowed(a, s_nums, roll):
            return 0
        
        return len(a)

    def _reward_function_dynamic(self, s, a):
        s_nums, roll = s
        if not self.allowed(a, s_nums, roll):
            return 0
        
        return len(a)
    
    def two_dice_dist(self, x):
        if x <= 1 or x > 12:
            return 0
        prob = [0, 0, 0.0278, 0.0556, 0.0833, 0.1111, 0.1389, 0.1667, 0.1389, 0.1111, 0.0833, 0.0556, 0.0278]
    
        return prob[int(x)]
            
    
def calc_state_space(choices=12):
    sum = 0
    sum2 = 0
    for i in range(13):
        combos = math.factorial(choices) // (math.factorial(choices - i)  * math.factorial(i))
        sum += combos
        sum2 += int(scipy.special.comb(12, i))
        
    print(sum)
    print(sum2)

def main():
    # game = BoxGame()
    # game.game_loop()
    calc_state_space()

if __name__ == "__main__":
    main()