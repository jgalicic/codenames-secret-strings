import random
import time

def color_gen():
    random.seed(time.clock())
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
# print(color_gen())

alpha = ['a','b','z','v','e','f','g','x','i','j']

test_date = time.strftime('%Y-%m-%d %H:%M:%S')

code = test_date.replace(' ', '').replace('-', '').replace(':','')
alpha_code = ''

for i in range(6,len(code)):
    num = int(code[i])
    alpha_code += alpha[num]

print(test_date)
print(code)
print(alpha_code)

decode = ''
for letter in alpha_code:
    for idx in range(len(alpha)):
        if alpha[idx] == letter:
            decode += str(idx)
decode = int(decode)

print(decode)
#test comment