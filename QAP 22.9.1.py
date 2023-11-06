array = list(map(int, input('Введите последовательность целых чисел в произвольном порядке через пробел:').split()))

def sort_by_ascend(array):
    for i in range(len(array)):
        idx_min = i
        for j in range(i, len(array)):
            if array[j] < array[idx_min]:
                idx_min = j
        if i != idx_min:
            array[i], array[idx_min] = array[idx_min], array[i]
    return array

print(f'Последовательность отсортирована по возрастанию в следующем виде: {sort_by_ascend(array)}')

while True:
    try:
        element = int(input("Введите любое положительное целое число из полученного списка: "))
        if element < min(array) or element > max(array):
            print("Указанное число не входит в диапазон списка!")
        if element <= 0:
            raise Exception
        break
    except ValueError:
        print("Нужно ввести целое число!")
    except Exception:
        print("Нужно ввести положительное число!")

def binary_search(array, element, left, right):
    if left > right:
        return False
    middle = (right + left) // 2
    if array[middle] == element:
        return middle
    elif element < array[middle]:
        return binary_search(array, element, left, middle - 1)
    else:
        return binary_search(array, element, middle + 1, right)

if not binary_search(array, element, 0, len(array) - 1):
    print(f"Указанный элемент {element} отсутствует в последовательности.")
else:
    print(f"Индекс числа {element} в отсортированной последовательности равен: \
{binary_search(array, element, 0, len(array) - 1)}")