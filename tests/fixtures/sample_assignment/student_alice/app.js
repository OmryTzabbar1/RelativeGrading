// Simple Todo App
const todoList = [];

function addTodo(text) {
  todoList.push({ id: Date.now(), text, completed: false });
  saveToLocalStorage();
}

function deleteTodo(id) {
  const index = todoList.findIndex(todo => todo.id === id);
  if (index > -1) {
    todoList.splice(index, 1);
    saveToLocalStorage();
  }
}

function updateTodo(id, text) {
  const todo = todoList.find(todo => todo.id === id);
  if (todo) {
    todo.text = text;
    saveToLocalStorage();
  }
}

function saveToLocalStorage() {
  localStorage.setItem('todos', JSON.stringify(todoList));
}

function loadFromLocalStorage() {
  const stored = localStorage.getItem('todos');
  if (stored) {
    todoList.push(...JSON.parse(stored));
  }
}

// Initialize
loadFromLocalStorage();
