from task_manager import TaskManager
import datetime

def main():
    task_manager = TaskManager()
    print(task_manager.load_from_file())

    while True:
        print("\n--- Gestionnaire de Tâches ---")
        print("1. Ajouter une tâche")
        print("2. Voir les tâches")
        print("3. Marquer une tâche comme terminée")
        print("4. Sauvegarder les tâches")
        print("5. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            title = input("Titre de la tâche : ")
            due_date_str = input("Date d'échéance (YYYY-MM-DD HH:MM) : ")
            description = input("Description (optionnel) : ")
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
                task_manager.add_task(title, due_date, description)
                print("Tâche ajoutée avec succès.")
            except ValueError:
                print("Format de date invalide. Réessayez.")
        elif choice == "2":
            include_completed = input("Inclure les tâches terminées ? (oui/non) : ").lower() == "oui"
            print(task_manager.list_tasks(include_completed))
        elif choice == "3":
            task_title = input("Titre de la tâche à marquer comme terminée : ")
            print(task_manager.mark_task_completed(task_title))
        elif choice == "4":
            print(task_manager.save_to_file())
        elif choice == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    main()
