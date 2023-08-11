import random

def generate_sequence(length):
    sequence = []
    choices = ['a', 'b', 'c', 'd', 'e']
    prev_choice = random.choice(choices)
    sequence.append(prev_choice)

    for _ in range(length - 1):
        if prev_choice == 'a':
            next_choice = random.choice(['a', 'b'])
        elif prev_choice == 'b':
            next_choice = random.choice(['a', 'b', 'c'])
        elif prev_choice == 'c':
            next_choice = random.choice(['b', 'c', 'd'])
        elif prev_choice == 'd':
            next_choice = random.choice(['c', 'd', 'e'])
        elif prev_choice == 'e':
            next_choice = random.choice(['d', 'e'])
        
        # Check if the next choice is the same as the previous two choices
        if len(sequence) >= 2 and sequence[-1] == sequence[-2] == next_choice:
            if next_choice == 'a':
                next_choice = 'b'
            elif next_choice == 'b':
                next_choice = random.choice(['a', 'c'])
            elif next_choice == 'c':
                next_choice = random.choice(['a', 'b', 'd'])
            elif next_choice == 'd':
                next_choice = random.choice(['a', 'b' 'c', 'e'])
            elif next_choice == 'e':
                next_choice = random.choice(['a', 'b' 'c', 'd'])
        
        sequence.append(next_choice)
        prev_choice = next_choice

    return ''.join(sequence)

def main():
    for i in range(1, 6):
        sequence_length = 100
        random_sequence = generate_sequence(sequence_length)
        with open(f'map_{i}.txt', 'w') as file:
            file.write(random_sequence)

if __name__ == "__main__":
    main()

