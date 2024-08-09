/* globals Chart:false */

(() => {
  'use strict'

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  })
})()

const editModal = document.getElementById('editModal');
if (editModal) {
  editModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    // Parse JSON string from data-bs-camera attribute
    const camera = JSON.parse(button.getAttribute('data-bs-camera'));

    // Update the modal's content
    const modalTitle = editModal.querySelector('.modal-title');
    const camera_id_input = editModal.querySelector('.camera-id input');
    const camera_name_input = editModal.querySelector('.camera-name input');
    const camera_url_input = editModal.querySelector('.camera-url input');

    modalTitle.textContent = `Editing ${camera._id}`;
    camera_id_input.value = camera._id;
    camera_name_input.value = camera.name;
    camera_url_input.value = camera.url;
  });
}

const deleteModal = document.getElementById('deleteModal');
if (deleteModal) {
  deleteModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    // Parse JSON string from data-bs-camera attribute
    const camera = JSON.parse(button.getAttribute('data-bs-camera'));

    // Update the modal's content
    const modalTitle = deleteModal.querySelector('.modal-title');
    const camera_id_input = deleteModal.querySelector('.camera-id input');
    const camera_name_input = deleteModal.querySelector('.camera-name input');

    modalTitle.textContent = `Deleting ${camera._id}`;
    camera_id_input.value = camera._id;
    camera_name_input.value = camera.name;
  });
}

const addModal = document.getElementById('addModal');
if (addModal) {
  addModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    // Update the modal's content
    const modalTitle = addModal.querySelector('.modal-title');
    const camera_id_input = addModal.querySelector('.camera-id input');
    const camera_name_input = addModal.querySelector('.camera-name input');
    const camera_url_input = addModal.querySelector('.camera-url input');

    modalTitle.textContent = 'Add Camera';
    camera_id_input.value = '';
    camera_name_input.value = '';
    camera_url_input.value = '';
  });
}

const addForm = document.getElementById('addForm');
if (addForm) {
  addForm.addEventListener('submit', async event => {
    event.preventDefault();
    const formData = new FormData(addForm);
    const response = await fetch('/cameras', {
      method: 'POST',
      body: formData
    });
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to add camera');
    }
  });
}

const editForm = document.getElementById('editForm');
if (editForm) {
  editForm.addEventListener('submit', async event => {
    event.preventDefault();
    const formData = new FormData(editForm);
    const response = await fetch('/cameras', {
      method: 'PUT',
      body: formData
    });
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to edit camera');
    }
  });
}

const deleteForm = document.getElementById('deleteForm');
if (deleteForm) {
  deleteForm.addEventListener('submit', async event => {
    event.preventDefault();
    const formData = new FormData(deleteForm);
    const response = await fetch('/cameras', {
      method: 'DELETE',
      body: formData
    });
    if (response.ok) {
      window.location.reload();
    } else {
      console.error('Failed to delete camera');
    }
  });
}

const logoutButton = document.getElementById('logoutButton');
if (logoutButton) {
  logoutButton.addEventListener('click', async event => {
    const response = await fetch('/logout', {
      method: 'POST'
    });
    if (response.ok) {
      window.location.href = '/';
    } else {
      console.error('Failed to logout');
    }
  });
}

const deleteAccountButton = document.getElementById('deleteAccountButton');
if (deleteAccountButton) {
  deleteAccountButton.addEventListener('click', async event => {
    const response = await fetch('/delete-account', {
      method: 'POST'
    });
    if (response.ok) {
      window.location.href = '/';
    } else {
      console.error('Failed to delete account');
    }
  });
}
