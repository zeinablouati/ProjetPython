import datetime
import json


class Task:
    """Représente une tâche unique."""

    def __init__(self, title, due_date, description=""):
        self.title = title
        self.due_date = due_date
        self.description = description
        self.is_completed = False

    def mark_completed(self):
        self.is_completed = True

    def __str__(self):
        status = "✔️" if self.is_completed else "❌"
        return f"{self.title} - {self.due_date.strftime('%Y-%m-%d %H:%M')} ({status})\n{self.description}"


class TaskManager:
    """Gère la liste des tâches."""

    def __init__(self):
        self.tasks = []

    def add_task(self, title, due_date, description=""):
        # C'est un TaskManager, add ou create aurait peut être suffit comme nom
        self.tasks.append(Task(title, due_date, description))

    def list_tasks(self, include_completed=False):
        # Pareil ici on se doute que ca va lister les Tasks et non autre chose
        # task_manager.get_list() ou task_manager.list() sonne peut être mieux que task_manager.list_tasks()
        if not self.tasks:
            return "Aucune tâche disponible."
        tasks_to_show = self.tasks if include_completed else [t for t in self.tasks if not t.is_completed]
        return "\n".join(str(task) for task in tasks_to_show) if tasks_to_show else "Aucune tâche en attente."

    def mark_task_completed(self, task_title):
        for task in self.tasks:
            if task.title == task_title:
                task.mark_completed()
                return f"Tâche '{task_title}' marquée comme terminée."
        return f"Aucune tâche trouvée avec le titre '{task_title}'."

    def save_to_file(self, file_name="tasks.json"):
        # Ici vous avez préféré task_manager.save_to_file() et non task_manager.save_tasks_to_file()
        with open(file_name, "w") as file:
            json.dump([t.__dict__ for t in self.tasks], file, default=str)
        return "Tâches sauvegardées dans le fichier."
        """Par contre du coup cela réécrit toutes les taches à chaque fois, ce n'est pas dérangeant pour l'instant
        mais si vous vous servez de l'application on peut assez vite avoir envie d'une fonction qui ajoute 1 seule
        tache type TaskManager().save(task, file) et pour tout réécrire TaskManager().save_all(file)
        """

    def load_from_file(self, file_name="tasks.json"):
        try:
            with open(file_name, "r") as file:
                tasks = json.load(file)
                # A priori on peut refermer le fichier ici
                # Les prochaines lignes n'ont pas besoin du fichier ouvert (et donc enlever l'indentation)
                self.tasks = [Task(t["title"], datetime.datetime.fromisoformat(t["due_date"]), t["description"]) for t in tasks]
                for task, data in zip(self.tasks, tasks):
                    task.is_completed = data["is_completed"]
            return "Tâches chargées depuis le fichier."
        except FileNotFoundError:
            return "Aucun fichier trouvé pour charger les tâches."

"""
D'un point de vue design, on aimerait pouvoir un jour enregistrer les tasks dans une base de données par exemple.
Vous allez créer une methode save_to_database et load_from_database, puis on aimerait aussi enregistrer dans un bucket AWS
save_to_bucket et load_from bucket etc.
En réalité les methodes devraient simplement s'appeler save et load. L'utilisateur du manager se fiche de savoir si c'est
enregistré dans une base de données, un fichier ou quoi que ce soit, il veut juste pouvoir save et load ses tasks.

On peut faire cela en "injectant" la dépendance au moment de l'initialisation du manager, typiquement
class TaskManagr:
    def __init__(self, repository):
        self.repository = repository
        self.tasks = []

    def save(self, task):
        self.repository.save(task)

Le repository étant par exemple une instance d'une classe DatabaseRepository ou d'une classe FileRepository

class Repository:
    def save(self):
        ...

    def load(self):
        ...


class FileRepository(Repository):
    def save(self, instance):
        logique pour sauvegarder l'instance dans un fichier

class DatabaseRepository(Repository):
    def save(self, instance):
        logique pour sauvegarder l'instance dans une base de données


Ici la classe Repository est ce qu'on appelle une interface, FileRepository et DatabaseRepository
sont des implémentations de cette interface. A l'initialisation d'un TaskManager (ou même dans la methode save),
on passe en argument soit un FileRepository soit un DatabaseRepository, peu importe tant que l'objet
implémente / respecte l'interface Repository, à savoir disposer d'une fonction save et d'une fonction load.

-> https://youtu.be/J1f5b4vcxCQ?si=N0M58kc8xhVovgmC

Python dispose d'un module ABC avec classes et méthodes abstraites https://docs.python.org/3/library/abc.html
Une classe abstraite est une classe qui ne peut pas être instanciée, elle doit être héritée par d'autres classes.

Une interface est un certain type de classe abstraite, en python on retrouve ce comportement avec la classe Protocol
https://peps.python.org/pep-0544/
"""
