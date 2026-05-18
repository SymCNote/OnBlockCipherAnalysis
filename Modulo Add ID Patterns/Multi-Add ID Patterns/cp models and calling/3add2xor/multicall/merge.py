


import os

count = [str(i) for i in range(10)] + ['a', 'b', 'c', 'd', 'e', 'f']
output = '3add5inNEW.txt'
files_name = [f"2add5inew{i}.txt" for i in count]

with open(output, 'w', encoding='utf-8') as out_f:
    for name in files_name:
        if os.path.exists(name):
            with open(name, 'r', encoding='utf-8') as in_f:
                out_f.write(in_f.read())
            print(f'merged: {name}')
        else:
            print(f'not found: {name}')

# print('finished →', output)