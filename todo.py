import json
import os

# Имя файла для хранения задач
FILE_NAME = "tasks.json"


def load_tasks():
    """Загружает задачи из файла."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    """Сохраняет задачи в файл."""
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def show_tasks():
    """Показывает список всех задач."""
    tasks = load_tasks()
    if not tasks:
        print("\nСписок задач пуст.")
    else:
        print("\nВаши задачи:")
        for i, task in enumerate(tasks, 1):
            status = "[x]" if task["done"] else "[ ]"
            print(f"{i}. {status} {task['title']}")


def add_task():
    """Добавляет новую задачу."""
    title = input("\nВведите описание задачи: ").strip()
    if not title:
        print("Описание не может быть пустым!")
        return

    tasks = load_tasks()
    new_task = {
        "title": title,
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Задача '{title}' добавлена.")


def complete_task():
    """Отмечает задачу как выполненную."""
    show_tasks()
    tasks = load_tasks()
    if not tasks:
        return

    try:
        num = int(input("\nВведите номер задачи для завершения: ")) - 1
        if 0 <= num < len(tasks):
            tasks[num]["done"] = True
            save_tasks(tasks)
            print(f"Задача '{tasks[num]['title']}' завершена!")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Нужно ввести число.")


def delete_task():
    """Удаляет задачу."""
    show_tasks()
    tasks = load_tasks()
    if not tasks:
        return

    try:
        num = int(input("\nВведите номер задачи для удаления: ")) - 1
        if 0 <= num < len(tasks):
            deleted_task = tasks.pop(num)
            save_tasks(tasks)
            print(f"Задача '{deleted_task['title']}' удалена.")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Нужно ввести число.")


def main():
    """Главная функция с меню."""
    while True:
        print("\n" + "=" * 30)
        print("МЕНЕДЖЕР ЗАДАЧ")
        print("=" * 30)
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Завершить задачу")
        print("4. Удалить задачу")
        print("5. Выход")

        choice = input("\nВыберите действие (1-5): ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()