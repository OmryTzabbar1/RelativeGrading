// Basic Todo App
let todos = [];

function addTodo(text) {
  todos.push({ text: text });
}

function deleteTodo(index) {
  todos.splice(index, 1);
}

function showTodos() {
  console.log(todos);
}
