from fasthtml.common import *
from sqlite_minutils.db import NotFoundError

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', hx_get=f'/toggle/{todo.id}', target_id=tid)
    delete = A('Delete', hx_delete=f'/{todo.id}', hx_swap='outerHTML', target_id=tid)
    return Li(toggle, delete, todo.title + (' ✅' if todo.done else ''), id=tid)

def make_input():
    return Input(placeholder='Add a new todo', id='title', hx_swap_oob='true')

app, rt, todos, Todo = fast_app('data/todos.db', live=False, title=str, done=bool, pk='id', render=render)


@rt('/')
def get():
    frm = Form(Group(make_input(), Button("Add")), hx_post='/', target_id='todo-list', hx_swap='beforeend')
    return Titled('Todos', Card(
        Ul(*todos(), id='todo-list'),
        header=frm
    ) )

@rt('/')
def post(todo:Todo): return todos.insert(todo), make_input()

@rt('/toggle/{tid}')
def get(tid: int):
    try:
        todo = todos[tid]
    except NotFoundError:
        return {"error": "Todo item not found"}, 404
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    todo.done = not todo.done
    todos.update(todo)
    return todo

@rt('/{tid}')
def delete(tid: int): todos.delete(tid)

serve()
