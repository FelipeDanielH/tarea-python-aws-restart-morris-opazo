from dataclasses import dataclass

import customtkinter as ctk

from aws_restart_lab.core.context import AppContext
from aws_restart_lab.core.exercise import ExerciseView


@dataclass
class Task:
    text: str
    done: bool = False


class TodoListView(ExerciseView):
    def __init__(self, master: ctk.CTkFrame, context: AppContext) -> None:
        super().__init__(master, context)
        self.tasks: list[Task] = []
        self.selected_index: int | None = None
        self.task_rows: list[ctk.CTkFrame] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=0, column=0, sticky="nsew", padx=36, pady=34)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_rowconfigure(3, weight=1)

        title = ctk.CTkLabel(
            workspace,
            text="Ejercicio 6",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            anchor="w",
        )
        title.grid(row=0, column=0, sticky="ew")

        self.task_entry = ctk.CTkEntry(
            workspace,
            height=44,
            corner_radius=8,
            border_color="#475569",
            fg_color="#0f2138",
            text_color="#ffffff",
            placeholder_text="Escribe una tarea...",
            placeholder_text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=15),
        )
        self.task_entry.grid(row=1, column=0, pady=(18, 12), sticky="ew")
        self.task_entry.bind("<Return>", lambda _event: self._add_or_update())

        actions = ctk.CTkFrame(workspace, fg_color="transparent")
        actions.grid(row=2, column=0, pady=(0, 14), sticky="ew")

        self.save_button = ctk.CTkButton(
            actions,
            text="Agregar",
            width=130,
            height=38,
            fg_color="#ff9900",
            hover_color="#e88900",
            text_color="#081526",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            command=self._add_or_update,
        )
        self.save_button.grid(row=0, column=0, padx=(0, 10))

        ctk.CTkButton(actions, text="Editar", width=110, height=38, command=self._edit_selected).grid(
            row=0, column=1, padx=10
        )
        ctk.CTkButton(actions, text="Eliminar", width=110, height=38, command=self._delete_selected).grid(
            row=0, column=2, padx=10
        )
        ctk.CTkButton(actions, text="Limpiar", width=110, height=38, command=self._reset_editor).grid(
            row=0, column=3, padx=10
        )

        self.list_frame = ctk.CTkScrollableFrame(
            workspace,
            fg_color="#081526",
            corner_radius=10,
            border_color="#334155",
            border_width=1,
        )
        self.list_frame.grid(row=3, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(
            workspace,
            text="0 tareas pendientes",
            text_color="#94a3b8",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            anchor="w",
        )
        self.status_label.grid(row=4, column=0, pady=(10, 0), sticky="ew")

    def _add_or_update(self) -> None:
        text = self.task_entry.get().strip()
        if not text:
            return

        if self.selected_index is None:
            self.tasks.append(Task(text=text))
        else:
            self.tasks[self.selected_index].text = text
        self._reset_editor()
        self._render_tasks()

    def _edit_selected(self) -> None:
        if self.selected_index is None:
            return
        self.task_entry.delete(0, "end")
        self.task_entry.insert(0, self.tasks[self.selected_index].text)
        self.save_button.configure(text="Guardar")

    def _delete_selected(self) -> None:
        if self.selected_index is None:
            return
        del self.tasks[self.selected_index]
        self._reset_editor()
        self._render_tasks()

    def _reset_editor(self) -> None:
        self.selected_index = None
        self.task_entry.delete(0, "end")
        self.save_button.configure(text="Agregar")

    def _toggle_done(self, index: int) -> None:
        self.tasks[index].done = not self.tasks[index].done
        self.selected_index = index
        self._render_tasks()

    def _select_task(self, index: int) -> None:
        self.selected_index = index
        self._render_tasks()

    def _render_tasks(self) -> None:
        for row in self.task_rows:
            row.destroy()
        self.task_rows.clear()

        if not self.tasks:
            empty = ctk.CTkLabel(
                self.list_frame,
                text="No hay tareas todavia.",
                text_color="#94a3b8",
                font=ctk.CTkFont(family="Segoe UI", size=16),
            )
            empty.grid(row=0, column=0, padx=18, pady=18, sticky="w")
            self.task_rows.append(empty)
            self.status_label.configure(text="0 tareas pendientes")
            return

        for index, task in enumerate(self.tasks):
            selected = index == self.selected_index
            row = ctk.CTkFrame(
                self.list_frame,
                fg_color="#132a46" if selected else "#0f2138",
                corner_radius=8,
            )
            row.grid(row=index, column=0, padx=12, pady=6, sticky="ew")
            row.grid_columnconfigure(1, weight=1)
            row.bind("<Button-1>", lambda _event, task_index=index: self._select_task(task_index))

            checkbox = ctk.CTkCheckBox(
                row,
                text="",
                width=28,
                command=lambda task_index=index: self._toggle_done(task_index),
            )
            checkbox.grid(row=0, column=0, padx=(12, 4), pady=10)
            if task.done:
                checkbox.select()

            label = ctk.CTkLabel(
                row,
                text=task.text,
                text_color="#94a3b8" if task.done else "#ffffff",
                font=ctk.CTkFont(family="Segoe UI", size=15),
                anchor="w",
            )
            label.grid(row=0, column=1, padx=8, pady=10, sticky="ew")
            label.bind("<Button-1>", lambda _event, task_index=index: self._select_task(task_index))
            self.task_rows.append(row)

        pending = sum(1 for task in self.tasks if not task.done)
        self.status_label.configure(text=f"{pending} tareas pendientes de {len(self.tasks)}")
