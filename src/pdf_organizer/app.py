from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .db import connect
from .platform_actions import open_path
from .repository import PdfRecord, PdfRepository
from .workspace import get_workspace_root, resolve_workspace_pdf_path


class PdfOrganizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.workspace_root = get_workspace_root()
        self.connection = connect(self.workspace_root)
        self.repository = PdfRepository(self.connection, self.workspace_root)
        self.selected_record_id: int | None = None
        self.show_missing = tk.BooleanVar(value=False)
        self.search_text = tk.StringVar()
        self.search_text.trace_add("write", lambda *_: self.refresh_records())

        self.root.title("PDF Organizer")
        self.root.geometry("1100x720")
        self.root.minsize(980, 640)

        self._build_ui()
        self.refresh_all()

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=4)
        self.root.rowconfigure(1, weight=1)

        header = ttk.Frame(self.root, padding=16)
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="PDF Organizer", font=("TkHeadingFont", 20, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text=f"Workspace: {self.workspace_root}",
            font=("TkDefaultFont", 10),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(6, 0))
        ttk.Button(header, text="Link PDF", command=self.link_pdf).grid(row=0, column=2, sticky="e")

        left = ttk.Frame(self.root, padding=(16, 0, 8, 16))
        left.grid(row=1, column=0, sticky="nsew")
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)

        search_row = ttk.Frame(left)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        search_row.columnconfigure(1, weight=1)
        ttk.Label(search_row, text="Search").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Entry(search_row, textvariable=self.search_text).grid(row=0, column=1, sticky="ew")
        ttk.Checkbutton(
            search_row,
            text="Show missing",
            variable=self.show_missing,
            command=self.refresh_records,
        ).grid(row=0, column=2, sticky="e", padx=(12, 0))

        ttk.Label(left, text="PDF Records", font=("TkHeadingFont", 12, "bold")).grid(
            row=1, column=0, sticky="w"
        )
        self.record_list = tk.Listbox(left, exportselection=False)
        self.record_list.grid(row=2, column=0, sticky="nsew", pady=(8, 0))
        self.record_list.bind("<<ListboxSelect>>", self.on_select_record)

        right = ttk.Frame(self.root, padding=(8, 0, 16, 16))
        right.grid(row=1, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        detail_header = ttk.Frame(right)
        detail_header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        detail_header.columnconfigure(0, weight=1)
        ttk.Label(detail_header, text="Record Details", font=("TkHeadingFont", 12, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        actions = ttk.Frame(detail_header)
        actions.grid(row=0, column=1, sticky="e")
        ttk.Button(actions, text="Open File", command=self.open_file).grid(row=0, column=0, padx=(0, 6))
        ttk.Button(actions, text="Open Folder", command=self.open_folder).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(actions, text="Delete Record", command=self.delete_record).grid(row=0, column=2)

        editor = ttk.Frame(right)
        editor.grid(row=1, column=0, sticky="nsew")
        editor.columnconfigure(1, weight=1)
        editor.rowconfigure(5, weight=1)

        ttk.Label(editor, text="Title").grid(row=0, column=0, sticky="nw", pady=(0, 8))
        self.title_var = tk.StringVar()
        ttk.Entry(editor, textvariable=self.title_var).grid(row=0, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(editor, text="Description").grid(row=1, column=0, sticky="nw", pady=(0, 8))
        self.description_text = tk.Text(editor, height=8, wrap="word")
        self.description_text.grid(row=1, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(editor, text="Path").grid(row=2, column=0, sticky="nw", pady=(0, 8))
        self.path_var = tk.StringVar()
        ttk.Label(editor, textvariable=self.path_var, wraplength=480).grid(row=2, column=1, sticky="w", pady=(0, 8))

        ttk.Label(editor, text="Status").grid(row=3, column=0, sticky="nw", pady=(0, 8))
        self.status_var = tk.StringVar()
        ttk.Label(editor, textvariable=self.status_var).grid(row=3, column=1, sticky="w", pady=(0, 8))

        ttk.Label(editor, text="Assigned Tags").grid(row=4, column=0, sticky="nw", pady=(0, 8))
        self.assigned_tags_var = tk.StringVar()
        ttk.Label(editor, textvariable=self.assigned_tags_var, wraplength=480).grid(
            row=4, column=1, sticky="w", pady=(0, 8)
        )

        tag_editor = ttk.Frame(editor)
        tag_editor.grid(row=5, column=1, sticky="nsew")
        tag_editor.columnconfigure(0, weight=1)
        tag_editor.rowconfigure(1, weight=1)
        ttk.Label(tag_editor, text="Global Tags", font=("TkHeadingFont", 11, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.tag_list = tk.Listbox(tag_editor, selectmode=tk.MULTIPLE, exportselection=False)
        self.tag_list.grid(row=1, column=0, sticky="nsew", pady=(8, 8))

        tag_actions = ttk.Frame(tag_editor)
        tag_actions.grid(row=2, column=0, sticky="ew")
        tag_actions.columnconfigure(0, weight=1)
        self.new_tag_var = tk.StringVar()
        ttk.Entry(tag_actions, textvariable=self.new_tag_var).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(tag_actions, text="Add Tag", command=self.add_tag).grid(row=0, column=1, padx=(0, 6))
        ttk.Button(tag_actions, text="Remove Tag", command=self.remove_tag).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(tag_actions, text="Apply To Record", command=self.apply_tags_to_record).grid(row=0, column=3)

        ttk.Button(editor, text="Save Changes", command=self.save_record).grid(
            row=6, column=1, sticky="e", pady=(16, 0)
        )

    def refresh_all(self) -> None:
        self.refresh_tags()
        self.refresh_records()

    def refresh_records(self) -> None:
        include_missing = self.show_missing.get()
        records = self.repository.list_records(self.search_text.get(), include_missing=include_missing)
        self.records_by_list_index = records
        self.record_list.delete(0, tk.END)
        for record in records:
            suffix = " [Missing]" if not record.file_exists else ""
            self.record_list.insert(tk.END, f"{record.title}{suffix}")
        if self.selected_record_id is not None:
            for index, record in enumerate(records):
                if record.id == self.selected_record_id:
                    self.record_list.selection_clear(0, tk.END)
                    self.record_list.selection_set(index)
                    self.record_list.activate(index)
                    self.populate_record(record)
                    break

    def refresh_tags(self) -> None:
        tags = self.repository.list_tags()
        self.tag_list.delete(0, tk.END)
        for tag in tags:
            self.tag_list.insert(tk.END, tag)

    def on_select_record(self, _event: object) -> None:
        selection = self.record_list.curselection()
        if not selection:
            return
        record = self.records_by_list_index[selection[0]]
        self.selected_record_id = record.id
        self.populate_record(record)

    def populate_record(self, record: PdfRecord) -> None:
        self.title_var.set(record.title)
        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", record.description)
        self.path_var.set(record.relative_path)
        self.status_var.set(record.status)
        self.assigned_tags_var.set(", ".join(record.tags) if record.tags else "No tags")

        self.tag_list.selection_clear(0, tk.END)
        tag_lookup = set(record.tags)
        for index, tag in enumerate(self.repository.list_tags()):
            if tag in tag_lookup:
                self.tag_list.selection_set(index)

    def current_record(self) -> PdfRecord | None:
        if self.selected_record_id is None:
            return None
        try:
            return self.repository.get_record(self.selected_record_id)
        except KeyError:
            self.selected_record_id = None
            return None

    def link_pdf(self) -> None:
        selected = filedialog.askopenfilename(
            parent=self.root,
            title="Select PDF",
            initialdir=str(self.workspace_root),
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if not selected:
            return
        try:
            record = self.repository.add_pdf(selected)
        except (ValueError, OSError) as exc:
            messagebox.showerror("Cannot link PDF", str(exc), parent=self.root)
            return
        except Exception as exc:
            messagebox.showerror("Cannot link PDF", f"Failed to create record: {exc}", parent=self.root)
            return
        self.selected_record_id = record.id
        self.refresh_all()

    def save_record(self) -> None:
        record = self.current_record()
        if record is None:
            messagebox.showinfo("No record selected", "Select a record before saving.", parent=self.root)
            return
        updated = self.repository.update_record(
            record.id,
            self.title_var.get(),
            self.description_text.get("1.0", tk.END),
        )
        self.populate_record(updated)
        self.refresh_records()

    def delete_record(self) -> None:
        record = self.current_record()
        if record is None:
            return
        confirmed = messagebox.askyesno(
            "Delete Record",
            f"Delete the record for '{record.title}' without deleting the PDF file?",
            parent=self.root,
        )
        if not confirmed:
            return
        self.repository.delete_record(record.id)
        self.selected_record_id = None
        self.title_var.set("")
        self.description_text.delete("1.0", tk.END)
        self.path_var.set("")
        self.status_var.set("")
        self.assigned_tags_var.set("")
        self.refresh_records()

    def add_tag(self) -> None:
        try:
            self.repository.create_tag(self.new_tag_var.get())
        except Exception as exc:
            messagebox.showerror("Cannot add tag", str(exc), parent=self.root)
            return
        self.new_tag_var.set("")
        self.refresh_tags()

    def remove_tag(self) -> None:
        selection = self.tag_list.curselection()
        if not selection:
            messagebox.showinfo("No tag selected", "Select a global tag to remove.", parent=self.root)
            return
        for index in reversed(selection):
            self.repository.delete_tag(self.tag_list.get(index))
        self.refresh_all()

    def apply_tags_to_record(self) -> None:
        record = self.current_record()
        if record is None:
            messagebox.showinfo("No record selected", "Select a record before applying tags.", parent=self.root)
            return
        selected_tags = [self.tag_list.get(index) for index in self.tag_list.curselection()]
        updated = self.repository.set_record_tags(record.id, selected_tags)
        self.populate_record(updated)
        self.refresh_records()

    def open_file(self) -> None:
        record = self.current_record()
        if record is None:
            return
        path = resolve_workspace_pdf_path(record.relative_path, self.workspace_root)
        if not path.exists():
            messagebox.showerror("Missing PDF", "The linked PDF cannot be found on disk.", parent=self.root)
            self.refresh_records()
            return
        open_path(path)

    def open_folder(self) -> None:
        record = self.current_record()
        if record is None:
            return
        path = resolve_workspace_pdf_path(record.relative_path, self.workspace_root)
        target = path.parent if path.exists() else self.workspace_root
        open_path(target)


def run() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    PdfOrganizerApp(root)
    root.mainloop()

