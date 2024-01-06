const deleteButton = document.querySelector('.delete-listing');
const confirmDeleteModal = document.querySelector('.confirm-delete-modal')
const acceptModalButton = document.querySelector('.modal-yes')
const cancelModalButton = document.querySelector('.modal-cancel')

const handleCloseModal = () => {
  confirmDeleteModal.classList.toggle('show')
}

deleteButton.addEventListener('click', handleCloseModal)
acceptModalButton.addEventListener('click', handleCloseModal)
cancelModalButton.addEventListener('click', handleCloseModal)

