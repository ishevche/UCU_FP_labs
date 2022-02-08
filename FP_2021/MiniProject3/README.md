# Filler

### Хід алгоритму

1. Робота алгоритму починається з фунуціі main(), яка не приймає жодного
   аргументу та є основною, з якої починається весь алгоритм

```python
first_player = get_current_player()
try:
    while True:
        make_move(first_player)
except EOFError:
    pass
```

2. Функція make_move(first_player) виконує основну логіку модулю - робить хід
   фикористовуючи допоміжні функції. Приймає аргументом інформацію про номер
   гравця.

```python
field: list = []
opponent_cells = read_field(field, first_player)
for opponent_cell in opponent_cells:
    calculate_distance(field, opponent_cell)
figure, figure_size, shift = get_piece()
figure = choose_figure(field, figure, figure_size, first_player)
print(f'{figure[0] - shift[0]} {figure[1] - shift[1]}')
```

3. Функція read_field(field, first_player) зчитує поле та записує у передану
   першим вргументом змінну. Також отримує інформацію про номер гравця. Усі
   пусті клітинки на полі заміняє на -1. Повертає сет, кожен елемент якого -
   координати клітинок супротивника.

```python
rows, cols = get_size()

opponent_symbols = 'Xx' if first_player else 'Oo'

input()  # header skip

opponent_cells = set()

for row_idx in range(rows):
    row = input()[4:]
    row_list = []
    for col_idx in range(cols):
        if row[col_idx] == '.':
            row_list.append(-1)
        else:
            row_list.append(row[col_idx].upper())
            if row[col_idx] in opponent_symbols:
                opponent_cells.add((row_idx, col_idx))
    field.append(row_list)

return opponent_cells
```

4. Фунуція calculate_distance(field, start) є імплементацією bfs. Знаходить для
   кожної клітинки на полі, до яких можна дібратися не ступаючи на зайняті та
   переходячи тільки по ребрам, мінімальну відстань до заданої.

```python
fifo_queue = collections.deque()
fifo_queue.append(start)
while fifo_queue:
    row, col = fifo_queue.popleft()
    distance = field[row][col]
    if isinstance(distance, str):
        distance = 0
    neighbors = get_empty_neighbors(field, row, col)
    for new_row, new_col in neighbors:
        if field[new_row][new_col] == -1 or
                field[new_row][new_col] > distance + 1:
            field[new_row][new_col] = distance + 1
            fifo_queue.append((new_row, new_col))
```

5. Функція choose_figure(field, figure, size, first_player) пробігає по усім
   можливим варіантам поставити фігуру та обирає ту з них, яка має найменшу
   вартість - ту, сумарна відстань в кожній клітинці до опонента найменша.

```python
min_cost = -1
best_figure = 0, 0
for row in range(len(field) - size[0]):
    for col in range(len(field[row]) - size[1]):
        cost = get_cost(field, figure, row, col, first_player)
        if cost < 0:
            continue
        if cost < min_cost or min_cost == -1:
            min_cost = cost
            best_figure = row, col
return best_figure
```

## Приклад роботи

Приклад гри мого бота проти бота мого однокурсника Олексія Митника,
візуалізовано за допомогою програми яку він розробив:
![Image](./visualizer/res.gif)