#-------------------------------------------------------------------------------
# todo.py
# This project allow the user to create and manage a to-do list
# Author: Leonardo Valladares
# Date: 2025-09-06
#------------------------------------------------------------------------------

# Create an empty dictionary to store tasks and their completion status
tasks = []

# Variable to control the input loop
completed_loop = 0

# Welcome message
print("\nWelcome to the To-Do List Manager!")

# This loop manages all the interactions with the user
while completed_loop == 0: 
    check_input = 0
    selection = 0

    # This loop provides the option to the user and checks the input value
    while check_input == 0:    
        # Display menu options
        selection = input("\nMenu:\n" +
                            "1. Add Task\n" +
                            "2. Remove task\n" + 
                            "3. Mark task as complete\n" +
                            "4. View tasks\n" +
                            "5. Quit\n" +
                            "Choose an option: ")
        
        # Catch wrong inputs
        try:
            selection = int(selection)  # Convert input to integer
            if selection > 0 and selection < 6:
                check_input = 1
            else:
                print("Invalid input. Please enter a number from 1 to 5.\n")
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 5.\n")

        # Process the user's selection
        # Add task
        if selection == 1:
            task = input("Enter new task: ").title()            # Get the task from the user and capitalize it
            tasks.append({"task": task, "completed": False})    # Add the task as a dictionary with a completion status
            print(f'Task "{task}" added to the list.')

        # Remove task
        elif selection == 2:
            # Check if there are tasks to remove
            if not tasks:
                print("No tasks to remove.")                
            else:
                # Display tasks with numbers
                for i, task in enumerate(tasks, 1):
                    status = "✓" if task["completed"] else "✗" # Check if task is completed
                    print(f"{i}. [{status}] {task['task']}") 
                try:
                    task_num = int(input("Enter the number of the task to remove: "))
                    if 1 <= task_num <= len(tasks):
                        removed_task = tasks.pop(task_num - 1)  # Remove the task from the list
                        print(f'Task "{removed_task["task"]}" removed from the list.')
                    else:
                        print("Invalid task number.")
                except ValueError:                              # Catch wrong inputs
                    print("Please enter a valid number.")
        
        # mark task as complete
        elif selection == 3:   
            if not tasks:
                print("No tasks to mark as complete.")
            else:
                # Display tasks with numbers
                for i, task in enumerate(tasks, 1):
                    status = "✓" if task["completed"] else "✗" # Check if task is completed
                    print(f"{i}. [{status}] {task['task']}")
                try:
                    task_num = int(input("Enter the number of the task to mark as complete: "))
                    if 1 <= task_num <= len(tasks):
                        tasks[task_num - 1]["completed"] = True  # Mark the task as complete
                        print(f'Task "{tasks[task_num - 1]["task"]}" marked as complete.')
                        # legend   
                        print("\nLegend: ✓ = Completed, ✗ = Not Completed")
                    else:
                        print("Invalid task number.")
                except ValueError:                               # Catch wrong inputs
                    print("Please enter a valid number.")
        
        # View tasks
        elif selection == 4:
            if not tasks:
                print("\nNo tasks in the list.")
            else:
                print("\nYour To-Do List:")
                for i, task in enumerate(tasks, 1):
                    status = "✓" if task["completed"] else "✗"
                    print(f"{i}. [{status}] {task['task']}")
            # legend   
            print("\nLegend: ✓ = Completed, ✗ = Not Completed")
        
        # Quit the program
        elif selection == 5:
            completed_loop = 1 # Exit the loop


print("\nExiting the to-do list manager. Goodbye!")

