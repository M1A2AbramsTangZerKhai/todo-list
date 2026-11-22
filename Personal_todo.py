import json
import os

# The file where tasks are saved, so they are still there next time you run the program
FILENAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "todo_list.json"
)

def load_tasks():
    # On the first run there is no save file yet, so start with an empty list instead of crashing
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # If the file is damaged or empty, starting fresh is safer than crashing
        return []


def save_tasks(tasks):
    # Called after every change so nothing is lost if the program closes unexpectedly
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)


def show_tasks(tasks):
    if len(tasks) == 0:
        print("\nYour to-do list is empty.")
        return

    print("\n=====Your To-Do List=====")
    # Start numbering at 1 because people count from 1, not 0
    for number, task in enumerate(tasks, start=1):
        if task["done"]:
            status = "[x]"
        else:
            status = "[ ]"
        print(f"{number}. {status} {task['title']}")


def add_task(tasks):
    title = input("Enter the new task: ").strip()
    # Reject blank input so the list doesn't fill up with empty tasks
    if title == "":
        print("Task cannot be empty.")
        return

    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")


def complete_task(tasks):
    if len(tasks) == 0:
        print("There are no tasks to complete.")
        return

    show_tasks(tasks)
    choice = input("Enter the number of the task to mark as done: ").strip()

    # isdigit() checks the input is a whole number, so int() below cannot crash
    if not choice.isdigit():
        print("Please enter a number.")
        return

    index = int(choice) - 1  # Lists start at 0, but the user sees numbers starting at 1
    if index < 0 or index >= len(tasks):
        print("Task number does not exist.")
        return

    tasks[index]["done"] = True
    save_tasks(tasks)
    print(f"Marked as done: {tasks[index]['title']}")


def delete_task(tasks):
    if len(tasks) == 0:
        print("There are no tasks to delete.")
        return

    show_tasks(tasks)
    choice = input("Enter the number of the task to delete: ").strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(tasks):
        print("That task number does not exist.")
        return

    # pop() removes the task and gives it back, so we can show its name in the message
    removed = tasks.pop(index)
    save_tasks(tasks)
    print(f"Deleted: {removed['title']}")


def main():
    tasks = load_tasks()

    # Loop until the user chooses to quit, so they can do many actions in one run
    while True:
        print("\n=====To-Do List Menu=====")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Mark a task as done")
        print("4. Delete a task")
        print("5. Quit")

        choice = input("Choose an option (1 ~ 5): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


# This makes main() run only when you run this file directly, not when another file imports it
if __name__ == "__main__":
    main()