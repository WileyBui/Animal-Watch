var exampleModal = document.getElementById('replyCommentModal')
exampleModal.addEventListener('show.bs.modal', function (event) {
    console.log("inside addEventListener")
    console.log(event)
})