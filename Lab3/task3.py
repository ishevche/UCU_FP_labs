string_input = input()
input_len = len(string_input)
int_input = int(string_input, base=2)
int_answer = int_input ^ (int_input >> 1)
string_answer = bin(int_answer)[2:]
answer_len = len(string_answer)
for i in range(input_len - len(string_answer)):
    print(0, end="")
print(string_answer)
