const deleteButtons = document.querySelectorAll('#deleteButton');
const editButtons = document.querySelectorAll('#editButton');
const checkboxes = document.querySelectorAll('.checkbox');
const navbarElements = document.querySelectorAll('.a');


// Event listeners for the checkboxex
checkboxes.forEach((checkbox) => {
  checkboxCheck(checkbox);
  checkbox.addEventListener('click', () => {
    const toDoId = checkbox.dataset.id;
    checkboxCheck(checkbox);
    checkToDo(toDoId);
  });
});


// Event listeners for the "Delete" buttons
deleteButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const toDoId = button.dataset.id;
    deleteToDo(toDoId);
  });
});


// Event listeners for the "Edit" buttons
editButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const toDoId = button.dataset.id;
    document.querySelector(`.checkbox-container-${toDoId}`).classList.add('hide');
    document.querySelector(`.todos-list-${toDoId}`).style.gridTemplateColumns = "100%";
    document.querySelector(`.edit-button-${toDoId}`).classList.add('hide');
    document.querySelector(`.delete-button-${toDoId}`).classList.add('hide');
    document.querySelector(`.date-text-${toDoId}`).classList.add('hide');
    document.querySelector(`.edit-form-${toDoId}`).classList.remove('hide');
    document.querySelector(`.edit-form-${toDoId}`).classList.add('show');
  });
});


// Applies styling to the active tab of the navbar
navbarElements.forEach(element => {
  if (element.href === location.href || element.href + '?next=%2F' === location.href) {
    element.classList.add("active-nav");
  } else {
    element.classList.remove("active-nav");
  }
});


// Sends post request to check/uncheck a ToDo
function checkToDo(toDoId) {
  fetch('/checkbox', {
    method: 'POST',
    body: JSON.stringify({ toDoId })
  }).then(() => window.location.href = '/')
}


// Sends post request to delete a ToDo
function deleteToDo(toDoId) {
  fetch('/delete-todo', {
    method: 'POST',
    body: JSON.stringify({ toDoId })
  }).then(() => window.location.href = '/')
}


// Checks if a ToDo is done
function checkboxCheck(checkbox) {
  const toDoId = checkbox.dataset.id;
  toDoStatus = checkbox.checked;
  if (toDoStatus) {
    document.querySelector(`.todo-text-${toDoId}`).classList.add('checked');
  } else {
    document.querySelector(`.todo-text-${toDoId}`).classList.remove('checked');
  }
}