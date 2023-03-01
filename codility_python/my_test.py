def display_summary(summary):
    largest = 0
    longest_name = 0
    for tuple_ in summary:
        if longest_name < len(tuple_[0]):
            longest_name = len(tuple_[0])
        if largest < tuple_[1]:
            largest = tuple_[1]

    longest = len(str(largest))
    for j, tuple_ in enumerate(summary, start=1):
        name = tuple_[0]
        while len(name) < longest_name:
            name = ' ' + name

        answer = tuple_[1]
        while len(str(answer)) < longest:
            answer = ' ' +  answer

        print(f'{j}, {name} - {answer}: Time Consumed: {tuple_[2]}')

