document.addEventListener('DOMContentLoaded', (event) => {
    // Get the modal
    var modal = document.getElementById("Disclaimer");

    // Get the <span> element that closes the modal
    var span = document.getElementById("closeModal");

    // Check if the modal has been shown before in this session
    if (!sessionStorage.getItem('modalShown')) {
        // Show the modal
        modal.style.display = "block";

        // Set the flag in session storage
        sessionStorage.setItem('modalShown', 'true');
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});