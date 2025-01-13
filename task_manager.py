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
        self.tasks.append(Task(title, due_date, description))

    def list_tasks(self, include_completed=False):
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
        with open(file_name, "w") as file:
            json.dump([t.__dict__ for t in self.tasks], file, default=str)
        return "Tâches sauvegardées dans le fichier."

    def load_from_file(self, file_name="tasks.json"):
        try:
            with open(file_name, "r") as file:
                tasks = json.load(file)
                self.tasks = [Task(t["title"], datetime.datetime.fromisoformat(t["due_date"]), t["description"]) for t in tasks]
                for task, data in zip(self.tasks, tasks):
                    task.is_completed = data["is_completed"]
            return "Tâches chargées depuis le fichier."
        except FileNotFoundError:
            return "Aucun fichier trouvé pour charger les tâches."
