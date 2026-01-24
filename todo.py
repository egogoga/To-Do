# todo.py - Менеджер задач с дедлайном

import json
import os
from datetime import datetime

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
    """Показывает список всех задач с дедлайном."""
    tasks = load_tasks()
    if not tasks:
        print("\nСписок задач пуст.")
    else:
        print("\n" + "=" * 50)
        print(f"{'№':<3} {'Статус':<6} {'Задача':<30} {'Дедлайн':<12}")
        print("=" * 50)
        for i, task in enumerate(tasks, 1):
            status = "[✓]" if task["done"] else "[ ]"
            deadline = task.get("deadline", "Нет срока")
            title = task['title'][:27] + "..." if len(task['title']) > 27 else task['title']
            print(f"{i:<3} {status:<6} {title:<30} {deadline:<12}")


def add_task():
    """Добавляет новую задачу с дедлайном."""
    title = input("\nВведите описание задачи: ").strip()
    if not title:
        print("Описание не может быть пустым!")
        return

    deadline = input("Введите дедлайн (ГГГГ-ММ-ДД или Enter чтобы пропустить): ").strip()

    # Валидация даты
    if deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
            # Проверка, что дата не в прошлом
            if datetime.strptime(deadline, "%Y-%m-%d").date() < datetime.now().date():
                print("Внимание: дедлайн уже прошел!")
        except ValueError:
            print("Ошибка! Используйте формат ГГГГ-ММ-ДД. Дедлайн не установлен.")
            deadline = ""
    else:
        deadline = "Нет срока"

    tasks = load_tasks()
    new_task = {
        "title": title,
        "done": False,
        "deadline": deadline,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✓ Задача '{title}' добавлена. Дедлайн: {deadline}")


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
            tasks[num]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print(f"✓ Задача '{tasks[num]['title']}' завершена!")
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
            print(f"✗ Задача '{deleted_task['title']}' удалена.")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Нужно ввести число.")


def show_tasks_with_deadline():
    """Показывает задачи с ближайшим дедлайном."""
    tasks = load_tasks()
    if not tasks:
        print("\nСписок задач пуст.")
        return

    # Фильтруем задачи с дедлайном
    tasks_with_deadline = [t for t in tasks if t.get("deadline") and t["deadline"] != "Нет срока"]

    if not tasks_with_deadline:
        print("\nНет задач с установленным дедлайном.")
        return

    # Сортируем по дедлайну
    tasks_with_deadline.sort(key=lambda x: x["deadline"])

    print("\n" + "=" * 50)
    print("ЗАДАЧИ С ДЕДЛАЙНОМ (по ближайшей дате):")
    print("=" * 50)
    for i, task in enumerate(tasks_with_deadline, 1):
        status = "✓" if task["done"] else "✗"
        print(f"{i}. [{status}] {task['title']} → {task['deadline']}")


def main():
    """Главная функция с меню."""
    while True:
        print("\n" + "=" * 30)
        print(" МЕНЕДЖЕР ЗАДАЧ С ДЕДЛАЙНОМ")
        print("=" * 30)
        print("1. 📋 Показать все задачи")
        print("2. ➕ Добавить задачу")
        print("3. ✅ Завершить задачу")
        print("4. 🗑️  Удалить задачу")
        print("5. ⏰ Показать задачи с дедлайном")
        print("6. 🚪 Выход")

        choice = input("\nВыберите действие (1-6): ")

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            show_tasks_with_deadline()
        elif choice == "6":
            print("До свидания! Не забывайте про дедлайны!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()