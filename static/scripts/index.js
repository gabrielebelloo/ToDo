let deleteButtons = document.querySelectorAll('#deleteButton');
let editButtons = document.querySelectorAll('#editButton');
let checkboxes = document.querySelectorAll('.checkbox');

deleteButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const toDoId = button.dataset.id;
    deleteToDo(toDoId);
  });
});

editButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const toDoId = button.dataset.id;
    document.querySelector(`.checkbox-container-${toDoId}`).classList.add('hide');

    document.querySelector(`.todos-list-${toDoId}`).style.gridTemplateColumns = "100%";

    document.querySelector(`.edit-button-${toDoId}`).classList.add('hide');
    document.querySelector(`.delete-button-${toDoId}`).classList.add('hide');

    document.querySelector(`.edit-form-${toDoId}`).classList.remove('hide');
    document.querySelector(`.edit-form-${toDoId}`).classList.add('show');
  });
});

checkboxes.forEach((checkbox) => {
  checkboxCheck(checkbox);
  checkbox.addEventListener('click', () => {
    const toDoId = checkbox.dataset.id;
    checkboxCheck(checkbox);
    fetch('/checkbox', {
      method: 'POST',
      body: JSON.stringify({ toDoId })
    }).then(() => window.location.href = '/')
  });
});



function deleteToDo(toDoId) {
  fetch('/delete-todo', {
    method: 'POST',
    body: JSON.stringify({ toDoId })
  }).then(() => window.location.href = '/')
}


function checkboxCheck(checkbox) {
  const toDoId = checkbox.dataset.id;
  toDoStatus = checkbox.checked;
  if (toDoStatus) {
    document.querySelector(`.todo-text-${toDoId}`).classList.add('checked');
  } else {
    document.querySelector(`.todo-text-${toDoId}`).classList.remove('checked');
  }
}



navbarElements = document.querySelectorAll('.a');

navbarElements.forEach((element) => {
  if (element.href === location.href) {
    element.classList.add("active-nav");
  } else {
    element.classList.remove("active-nav");
  }
});
