# Gerenciador de tarefas refatorado com boas práticas

import json
import os
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


class Priority(Enum):
    """Enum para prioridades de tarefas"""
    LOW = "1"
    MEDIUM = "2"
    HIGH = "3"
    
    def get_label(self) -> str:
        labels = {"1": "BAIXA", "2": "MEDIA", "3": "ALTA"}
        return labels.get(self.value, "???")


@dataclass
class Task:
    """Representa uma tarefa com validação"""
    title: str
    description: str
    priority: str
    completed: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "titulo": self.title,
            "desc": self.description,
            "prio": self.priority,
            "feita": self.completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        return cls(
            title=data["titulo"],
            description=data["desc"],
            priority=data["prio"],
            completed=data["feita"]
        )


class TaskManager:
    """Gerencia operações de tarefas (lógica de negócio)"""
    
    def __init__(self, filename: str = "tarefas.json"):
        self.tasks: List[Task] = []
        self.filename = filename
    
    def add_task(self, title: str, description: str, priority: str) -> None:
        task = Task(title=title, description=description, priority=priority)
        self.tasks.append(task)
    
    def get_all_tasks(self) -> List[Task]:
        return self.tasks
    
    def mark_as_completed(self, index: int) -> bool:
        if self._is_valid_index(index):
            self.tasks[index].completed = True
            return True
        return False
    
    def delete_task(self, index: int) -> bool:
        if self._is_valid_index(index):
            self.tasks.pop(index)
            return True
        return False
    
    def update_task(self, index: int, title: Optional[str] = None, 
                    description: Optional[str] = None, priority: Optional[str] = None) -> bool:
        if not self._is_valid_index(index):
            return False
        
        task = self.tasks[index]
        if title:
            task.title = title
        if description:
            task.description = description
        if priority:
            task.priority = priority
        return True
    
    def filter_by_priority(self, priority: str) -> List[tuple[int, Task]]:
        return [(i, task) for i, task in enumerate(self.tasks) if task.priority == priority]
    
    def save_to_file(self) -> bool:
        try:
            with open(self.filename, "w") as f:
                data = [task.to_dict() for task in self.tasks]
                json.dump(data, f)
            return True
        except IOError:
            return False
    
    def load_from_file(self) -> bool:
        if not os.path.exists(self.filename):
            return False
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data]
            return True
        except (IOError, json.JSONDecodeError, KeyError):
            return False
    
    def _is_valid_index(self, index: int) -> bool:
        return 0 <= index < len(self.tasks)


class TaskUI:
    """Interface de usuário (separada da lógica)"""
    
    MENU_OPTIONS = {
        "1": "adicionar tarefa",
        "2": "listar tarefas",
        "3": "marcar como feita",
        "4": "deletar tarefa",
        "5": "editar tarefa",
        "6": "filtrar por prioridade",
        "7": "salvar em arquivo",
        "8": "carregar de arquivo",
        "0": "sair"
    }
    
    def __init__(self, manager: TaskManager):
        self.manager = manager
    
    def display_menu(self) -> None:
        print("\n" + "="*50)
        print("GERENCIADOR DE TAREFAS")
        print("="*50)
        for key, value in self.MENU_OPTIONS.items():
            print(f"{key} - {value}")
        print("="*50)
    
    def get_user_choice(self) -> str:
        return input("opcao: ")
    
    def display_task(self, index: int, task: Task, show_description: bool = True) -> None:
        status = "[X]" if task.completed else "[ ]"
        priority_label = Priority(task.priority).get_label()
        print(f"{index + 1}. {status} {task.title} - {priority_label}")
        if show_description:
            print(f"   {task.description}")
    
    def display_all_tasks(self, show_description: bool = True) -> None:
        tasks = self.manager.get_all_tasks()
        if not tasks:
            print("nenhuma tarefa")
            return
        
        for i, task in enumerate(tasks):
            self.display_task(i, task, show_description)
    
    def get_task_index(self) -> Optional[int]:
        try:
            number = input("numero da tarefa: ")
            return int(number) - 1
        except ValueError:
            return None
    
    def handle_add_task(self) -> None:
        title = input("titulo: ")
        description = input("descricao: ")
        priority = input("prioridade (1-baixa, 2-media, 3-alta): ")
        
        self.manager.add_task(title, description, priority)
        print("tarefa adicionada!")
    
    def handle_list_tasks(self) -> None:
        self.display_all_tasks(show_description=True)
    
    def handle_mark_completed(self) -> None:
        if not self.manager.get_all_tasks():
            print("nenhuma tarefa")
            return
        
        self.display_all_tasks(show_description=False)
        index = self.get_task_index()
        
        if index is not None and self.manager.mark_as_completed(index):
            print("marcada como feita!")
        else:
            print("invalido")
    
    def handle_delete_task(self) -> None:
        if not self.manager.get_all_tasks():
            print("nenhuma tarefa")
            return
        
        self.display_all_tasks(show_description=False)
        index = self.get_task_index()
        
        if index is not None and self.manager.delete_task(index):
            print("deletada!")
        else:
            print("invalido")
    
    def handle_edit_task(self) -> None:
        if not self.manager.get_all_tasks():
            print("nenhuma tarefa")
            return
        
        for i, task in enumerate(self.manager.get_all_tasks()):
            print(f"{i + 1}. {task.title}")
        
        index = self.get_task_index()
        if index is None or not self.manager._is_valid_index(index):
            print("invalido")
            return
        
        task = self.manager.get_all_tasks()[index]
        
        print(f"atual: {task.title}")
        new_title = input("novo titulo (enter para manter): ")
        
        print(f"atual: {task.description}")
        new_description = input("nova desc (enter para manter): ")
        
        print(f"atual: {task.priority}")
        new_priority = input("nova prio (enter para manter): ")
        
        self.manager.update_task(
            index,
            title=new_title or None,
            description=new_description or None,
            priority=new_priority or None
        )
        print("atualizada!")
    
    def handle_filter_by_priority(self) -> None:
        priority = input("prioridade (1/2/3): ")
        filtered_tasks = self.manager.filter_by_priority(priority)
        
        if not filtered_tasks:
            print("nenhuma tarefa com essa prioridade")
            return
        
        for index, task in filtered_tasks:
            self.display_task(index, task, show_description=False)
    
    def handle_save(self) -> None:
        if self.manager.save_to_file():
            print(f"salvo em {self.manager.filename}")
        else:
            print("erro ao salvar")
    
    def handle_load(self) -> None:
        if self.manager.load_from_file():
            print("carregado!")
        else:
            print("arquivo nao existe")
    
    def handle_exit(self) -> bool:
        print("tchau!")
        return True


def sistema_tarefas():
    """Função principal refatorada - apenas orquestra o fluxo"""
    manager = TaskManager()
    ui = TaskUI(manager)
    
    action_map = {
        "1": ui.handle_add_task,
        "2": ui.handle_list_tasks,
        "3": ui.handle_mark_completed,
        "4": ui.handle_delete_task,
        "5": ui.handle_edit_task,
        "6": ui.handle_filter_by_priority,
        "7": ui.handle_save,
        "8": ui.handle_load,
    }
    
    while True:
        ui.display_menu()
        choice = ui.get_user_choice()
        
        if choice == "0":
            if ui.handle_exit():
                break
        elif choice in action_map:
            action_map[choice]()
        else:
            print("opcao invalida")


if __name__ == "__main__":
    sistema_tarefas()
