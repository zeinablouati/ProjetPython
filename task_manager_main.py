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

        print("""
        --- Gestionnaire de Tâches ---
        1. Ajouter une tâche
        2. Voir les tâches
        3. Marquer une tâche comme terminée
        4. Sauvegarder les tâches
        5. Quitter
        """)

        choice = input("Choisissez une option : ")

        if choice == "1":
            title = input("Titre de la tâche : ")
            due_date_str = input("Date d'échéance (YYYY-MM-DD HH:MM) : ")
            description = input("Description (optionnel) : ")
            # Ce bout de logique appartient plutôt à la méthode add_task
            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
                task_manager.add_task(title, due_date, description)
                print("Tâche ajoutée avec succès.")
            except ValueError:
                print("Format de date invalide. Réessayez.")

            """On essaye de ne mettre dans le try que ce qui peut provoquer
            l'erreur que l'on gère ensuite dans l'except.
            le mot clé "else" (dans le contexte d'un try/except) gère uniquement le cas
            où il n'y a pas eu d'erreur et ne sera donc pas appelé s'il y a une ValueError :

            try:
                due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print("Format de date invalide. Réessayez.")
            else:
                task_manager.add_task(title, due_date, description)
                print("Tâche ajoutée avec succès.")

            En mettant la logique d'inputs dans la fonction add_task, celle ci pourrait provoquer
            une erreur au moment de formatter la date, cela donnerait donc qqchose comme:
            try:
                task_manager.add_task()
            except ValueError as e:
                print(e)
            else:
                print("Tâche ajoutée avec succès.")
            """

        elif choice == "2":
            include_completed = input("Inclure les tâches terminées ? (oui/non) : ").lower() == "oui"
            print(task_manager.list_tasks(include_completed))
        elif choice == "3":
            task_title = input("Titre de la tâche à marquer comme terminée : ")
            # Pareil ici l'input appartient à priori à la methode mark_task_completed
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
