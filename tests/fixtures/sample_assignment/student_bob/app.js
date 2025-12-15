// Enhanced Todo App with Dark Mode
class TodoApp {
  constructor() {
    this.todos = [];
    this.darkMode = false;
    this.init();
  }

  init() {
    this.loadFromLocalStorage();
    this.loadThemePreference();
  }

  addTodo(text) {
    if (!text || text.trim() === '') {
      throw new Error('Todo text cannot be empty');
    }
    const todo = {
      id: Date.now(),
      text: text.trim(),
      completed: false,
      createdAt: new Date().toISOString()
    };
    this.todos.push(todo);
    this.saveToLocalStorage();
    return todo;
  }

  deleteTodo(id) {
    const index = this.todos.findIndex(todo => todo.id === id);
    if (index === -1) {
      throw new Error('Todo not found');
    }
    this.todos.splice(index, 1);
    this.saveToLocalStorage();
  }

  updateTodo(id, text) {
    const todo = this.todos.find(todo => todo.id === id);
    if (!todo) {
      throw new Error('Todo not found');
    }
    if (!text || text.trim() === '') {
      throw new Error('Todo text cannot be empty');
    }
    todo.text = text.trim();
    todo.updatedAt = new Date().toISOString();
    this.saveToLocalStorage();
  }

  toggleComplete(id) {
    const todo = this.todos.find(todo => todo.id === id);
    if (todo) {
      todo.completed = !todo.completed;
      this.saveToLocalStorage();
    }
  }

  toggleDarkMode() {
    this.darkMode = !this.darkMode;
    localStorage.setItem('darkMode', this.darkMode);
    document.body.classList.toggle('dark-mode', this.darkMode);
  }

  saveToLocalStorage() {
    try {
      localStorage.setItem('todos', JSON.stringify(this.todos));
    } catch (error) {
      console.error('Failed to save todos:', error);
    }
  }

  loadFromLocalStorage() {
    try {
      const stored = localStorage.getItem('todos');
      if (stored) {
        this.todos = JSON.parse(stored);
      }
    } catch (error) {
      console.error('Failed to load todos:', error);
    }
  }

  loadThemePreference() {
    const stored = localStorage.getItem('darkMode');
    this.darkMode = stored === 'true';
    document.body.classList.toggle('dark-mode', this.darkMode);
  }

  filterTodos(filter) {
    switch (filter) {
      case 'active':
        return this.todos.filter(todo => !todo.completed);
      case 'completed':
        return this.todos.filter(todo => todo.completed);
      default:
        return this.todos;
    }
  }
}

// Initialize app
const app = new TodoApp();
