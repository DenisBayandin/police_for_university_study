import tkinter as tk

from dataclasses import fields, MISSING

from app.data_classes import *
from app.utils.errors import DbExecuteException


TABLES_ALREADY_CREATE = True
TIME_LIFE_NOTIFICATION = 3000
TABLES = {
    "Police Department": PoliceDepartment,
    "Technic": Technic,
    "Staff": Staff,
    "Personnel": Personnel,
    "Technic Department": TechnicDepartment,
    "Assignment": Assignment,
}


def create_tables():
    global TABLES_ALREADY_CREATE
    for table in TABLES.values():
        table.create_db_table()
        show_notification(f"{table.__name__.__str__()} created!")
    TABLES_ALREADY_CREATE = True
    window.after(TIME_LIFE_NOTIFICATION, clear_window_and_show_actions)


def drop_tables():
    global TABLES_ALREADY_CREATE
    for table in TABLES.values():
        table.drop_db_table()
        show_notification(f"{table.__name__.__str__()} dropped!")
    TABLES_ALREADY_CREATE = False
    window.after(TIME_LIFE_NOTIFICATION, clear_window_and_show_actions)


def show_notification(message, widget=None):
    if widget is None:
        notification = tk.Label(window, text=message, fg="green", font=("Arial", 16))
        notification.pack(pady=10)
        window.after(TIME_LIFE_NOTIFICATION, notification.destroy)
    else:
        notification = tk.Label(widget, text=message, fg="green", font=("Arial", 16))
        notification.pack(pady=10)
        window.after(TIME_LIFE_NOTIFICATION, notification.destroy)


def show_notification_about_error(message, widget=None):
    if widget is None:
        notification = tk.Label(window, text=message, fg="red", font=("Arial", 16))
        notification.pack(pady=10)
        window.after(TIME_LIFE_NOTIFICATION, notification.destroy)
    else:
        notification = tk.Label(widget, text=message, fg="red", font=("Arial", 16))
        notification.pack(pady=10)
        window.after(TIME_LIFE_NOTIFICATION, notification.destroy)


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def clear_window_and_show_actions():
    clear_window()
    show_action()


def create_scrollable_frame(table):
    show_action_for_table(table)
    canvas = tk.Canvas(window)
    v_scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar = tk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    h_scrollbar.pack(side="bottom", fill="x")
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    return scrollable_frame


def preview_for_create_table(table):
    clear_window()
    scrollable_frame = create_scrollable_frame(table)
    inputs = {}
    for field in fields(table):
        field_name = field.name
        label = tk.Label(
            scrollable_frame, text=field.name + (
                " *" if field.default is MISSING and field.default_factory is MISSING else ""
            )
        )
        label.pack()
        entry = tk.Entry(scrollable_frame)
        entry.pack()
        inputs[field_name] = entry
    submit_button = tk.Button(
        scrollable_frame,
        text="Create",
        command=lambda: create_record(table, inputs, scrollable_frame)
    )
    submit_button.pack()


def create_record(table, inputs, widget):
    data = {field: entry.get() for field, entry in inputs.items()}
    try:
        table(**data).create()
    except DbExecuteException as error:
        show_notification_about_error(f"An entry with such a key already exists: {error.__str__()}", widget)
    else:
        show_notification(f"The record has been created", widget)


def create_table_for_view(table, scrollable_frame):
    for col, header in enumerate([field.name for field in fields(table)]):
        label = tk.Label(scrollable_frame, text=header, relief="solid", width=20, height=2)
        label.grid(row=0, column=col)


def show_labels_for_pk(table, scrollable_frame):
    inputs = {}
    for field in table.pk():
        label = tk.Label(
            scrollable_frame, text=field.name + (
                " *" if field.default is MISSING and field.default_factory is MISSING else ""
            )
        )
        label.pack()
        entry = tk.Entry(scrollable_frame)
        entry.pack()
        inputs[field.name] = entry
        submit_button = tk.Button(
            scrollable_frame,
            text="Show",
            command=lambda: retrieve(table, inputs)
        )
        submit_button.pack()


def list_record(table):
    clear_window()
    show_action_for_table(table)
    scrollable_frame = create_scrollable_frame(table)
    create_table_for_view(table, scrollable_frame)
    try:
        records = table.list()
        if records:
            for row_index, row in enumerate(records, start=1):
                for col_index, value in enumerate(row):
                    label = tk.Label(scrollable_frame, text=value, relief="solid", width=20, height=2)
                    label.grid(row=row_index, column=col_index)
        show_notification(f"Success")
    except DbExecuteException as error:
        show_notification_about_error(f"An error occurred while retrieving the records: {error.__str__()}", scrollable_frame)


def preview_retrieve(table):
    try:
        clear_window()
        show_action_for_table(table)
        show_labels_for_pk(table, create_scrollable_frame(table))
    except DbExecuteException as error:
        show_notification_about_error(f"An error occurred while retrieving the record: {error.__str__()}")


def retrieve(table, inputs):
    data = {field: entry.get() for field, entry in inputs.items()}
    scrollable_frame = create_scrollable_frame(table)
    record = table.retrieve(**data)
    if record is None:
        label = tk.Label(
            window,
            text=f"No record found for {data}"
        )
        label.pack()
    else:
        create_table_for_view(table, scrollable_frame)
        for row_index, row in enumerate(record, start=1):
            for col_index, value in enumerate(row):
                label = tk.Label(scrollable_frame, text=value, relief="solid", width=20, height=2)
                label.grid(row=row_index, column=col_index)


def preview_update(table):
    clear_window()
    show_action_for_table(table)
    clear_window()
    scrollable_frame = create_scrollable_frame(table)
    inputs = {}
    for field in fields(table):
        field_name = field.name
        label = tk.Label(
            scrollable_frame, text=field.name + (
                " *" if field.default is MISSING and field.default_factory is MISSING else ""
            )
        )
        label.pack()
        entry = tk.Entry(scrollable_frame)
        entry.pack()
        inputs[field_name] = entry
    submit_button = tk.Button(
        scrollable_frame,
        text="Update",
        command=lambda: update_record(table, inputs, scrollable_frame)
    )
    submit_button.pack()


def update_record(table, inputs, widget):
    data = {field: entry.get() for field, entry in inputs.items()}
    pk_data = {field.name: data[field.name] for field in table.pk()}
    try:
        table.update(pk_data, **data)
    except DbExecuteException as error:
        show_notification_about_error(f"An error occurred while updating the record: {error.__str__()}", widget)
    else:
        show_notification(f"The record has been updated", widget)



def preview_delete(table):
    clear_window()
    show_action_for_table(table)
    scrollable_frame = create_scrollable_frame(table)
    inputs = {}
    for field in table.pk():
        field_name = field.name
        label = tk.Label(
            scrollable_frame, text=field.name + (
                " *" if field.default is MISSING and field.default_factory is MISSING else ""
            )
        )
        label.pack()
        entry = tk.Entry(scrollable_frame)
        entry.pack()
        inputs[field_name] = entry
    submit_button = tk.Button(
        scrollable_frame,
        text="Delete",
        command=lambda: delete_record(table, inputs, scrollable_frame)
    )
    submit_button.pack()


def delete_record(table, inputs, widget):
    data = {field: entry.get() for field, entry in inputs.items()}
    pk_data = {field.name: data[field.name] for field in table.pk()}
    try:
        table.delete(**pk_data)
    except DbExecuteException as error:
        show_notification_about_error(f"An error occurred when deleting the record: {error.__str__()}", widget)
    else:
        show_notification(f"The record has been deleted", widget)


def back_action(table):
    clear_window()
    show_action()


ACTION_FOR_TABLE = {
    "Retrieve": preview_retrieve,
    "List": list_record,
    "Create": preview_for_create_table,
    "Update": preview_update,
    "Delete": preview_delete,
    "Back": back_action
}


def show_action_for_table(table):
    clear_window()
    label = tk.Label(window, text=f"Actions for table: {table.__name__.__str__()}")
    label.pack(pady=10)
    for action_name, action in ACTION_FOR_TABLE.items():
        button = tk.Button(
            window,
            text=action_name,
            command=lambda a=action: a(table)
        )
        button.pack(pady=len(ACTION_FOR_TABLE))


def show_action():
    if TABLES_ALREADY_CREATE:
        actions = {"Destroy tables": drop_tables}
        for table_name, table in TABLES.items():
            button = tk.Button(
                window,
                text=table_name,
                command=lambda t=table: show_action_for_table(t)
            )
            button.pack(pady=len(TABLES))
    else:
        actions = {"Create tables": create_tables}
    for action_name, action in actions.items():
        action_button = tk.Button(
            window,
            text=action_name,
            command=lambda: action()
        )
        action_button.pack(pady=len(actions))


window = tk.Tk()
window.title("Police tables")
window.geometry("1000x1000")
show_action()
window.mainloop()
