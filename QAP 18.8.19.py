amount = 0
tickets = int(input("Введите количество билетов:\n"))
for age in range(tickets):
    age = int(input("Введите возраст посетителя:\n"))
    if age < 18:
        amount += 0
    elif age >= 18 and age <= 25:
        amount += 990
    elif age > 25:
        amount += 1390
if amount == 0:
    print("Проходите, детки, на конференцию!")
else:
    print("КОличество билетов:", tickets, "шт.")

if tickets > 3:
    discount = amount / 100 * 10
    print("Скидка составляет:", "%.2f" % discount, "руб.")
    print("К оплате, с учетом скидки:", "%.2f" % (amount -discount), "руб.")
if tickets < 4:
    Nodiscount = amount
    print("К оплате:", "%.2f" % Nodiscount, "руб." )