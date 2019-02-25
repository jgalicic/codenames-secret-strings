import random

def color_gen():
    done = False
    color_list = []
    brown_count = 5
    red_count = 5
    blue_count = 5
    black_count = 1

    while not done:
        num = random.randint(1,4)
        if num == 1 and brown_count > 0:
            color_list.append("brown")
            brown_count -= 1
        if num == 2 and red_count > 0:
            color_list.append("red")
            red_count -= 1
        if num == 3 and blue_count > 0:
            color_list.append("blue")
            blue_count -= 1
        if num == 4 and black_count > 0:
            color_list.append("black")
            black_count -= 1
        if black_count == 0 and red_count == 0 and brown_count == 0 and blue_count == 0:
            done = True

    print(color_list)
    print(len(color_list))
    return color_list
print(color_gen())