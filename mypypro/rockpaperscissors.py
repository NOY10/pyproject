import random
 
def play():
    user=input("R P S\n").lower()
    computer=random.choice(['r','p','s'])

    if user==computer:
        return "tie"
    elif win(user,computer):
        return "You won"
    return "computer won"

def win(user,computer):
    if (user=='r' and computer=='s') or (user=='s' and computer=='p') or (user=='p' and computer=='s'):
        return True
print(play())
 
