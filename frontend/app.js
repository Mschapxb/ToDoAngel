document.addEventListener('DOMContentLoaded', function () {
    function loadTodos() {
        fetch('http://localhost:8000')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.text(); // Change from json() to text() to handle empty responses
            })
            .then(text => {
                const data = text ? JSON.parse(text) : []; // Parse JSON only if text is not empty
                const list = document.getElementById('todo-list');
                list.innerHTML = '';
                data.forEach(todo => {
                    const li = document.createElement('li');
                    const dueDate = todo.due_date ? new Date(todo.due_date).toLocaleDateString() : 'No due date';
                    li.innerHTML = `
                        <input type="checkbox" ${todo.completed ? 'checked' : ''} onchange="toggleComplete(${todo.id}, this.checked)">
                        <span>${todo.content} - Due: ${dueDate}</span>
                        <button onclick="deleteTodo(${todo.id})">Delete</button>
                        <button onclick="editTodoPrompt(${todo.id}, '${todo.content}', '${todo.due_date}', ${todo.completed})">Edit</button>
                    `;
                    list.appendChild(li);
                });
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }

    document.getElementById('todo-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const input = document.getElementById('todo-input');
        const date = document.getElementById('todo-date');
        const content = input.value;
        const due_date = date.value;

        fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content, due_date })
        })
        .then(response => response.json())
        .then(data => {
            loadTodos();
            input.value = '';
            date.value = '';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    window.deleteTodo = function (id) {
        fetch(`http://localhost:8000?id=${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            loadTodos();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    window.editTodoPrompt = function (id, content, due_date, completed) {
        const newContent = prompt('Edit todo:', content);
        const newDueDate = prompt('Edit due date (YYYY-MM-DD):', due_date);
        const newCompleted = confirm('Is this task completed?');

        if (newContent !== null && newDueDate !== null) {
            window.editTodo(id, newContent, newDueDate, newCompleted);
        }
    };

    window.editTodo = function (id, content, due_date, completed) {
        fetch('http://localhost:8000', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id, content, due_date, completed })
        })
        .then(response => response.json())
        .then(data => {
            loadTodos();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    window.toggleComplete = function (id, completed) {
        fetch('http://localhost:8000', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id, completed })
        })
        .then(response => response.json())
        .then(data => {
            loadTodos();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    loadTodos();
});
