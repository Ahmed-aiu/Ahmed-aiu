// Function to get the current route or page identifier
function getPageIdentifier() {
    return window.location.pathname.replace(/\//g, "_");  // Convert '/' to '_' for valid cookie naming
}

// Function to set a cookie with a page-specific name
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to get a cookie with a page-specific name
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Event handler for when any modal is shown
function onModalShow(event) {
    var modalElement = event.target;
    if (modalElement && modalElement.id === 'helpModal') {
        // The help modal is being shown
        // Set the checkbox state based on the cookie
        var checkbox = modalElement.querySelector('#dontShowAgain');
        if (checkbox) {
            var checkboxStatusCookie = getCookie('dontShowModalCheckboxStatus');
            checkbox.checked = (checkboxStatusCookie === 'true');
        }
    }
}

// Event handler for when any modal is hidden
function onModalHide(event) {
    var modalElement = event.target;
    if (modalElement && modalElement.id === 'helpModal') {
        var checkbox = modalElement.querySelector('#dontShowAgain');
        var pageId = getPageIdentifier();  // Get unique identifier for the current page

        if (checkbox && checkbox.checked) {
            // Set a page-specific cookie to not show the modal again for this route
            setCookie('dontShowModal_' + pageId, 'true', 30);

            // Set a separate cookie to remember the checkbox state globally
            setCookie('dontShowModalCheckboxStatus', 'true', 30);
        } else {
            // If the checkbox is unchecked, clear the page-specific cookie and the checkbox status cookie
            setCookie('dontShowModal_' + pageId, '', -1);  // Clear the page-specific cookie
            setCookie('dontShowModalCheckboxStatus', '', -1);  // Clear the checkbox status cookie
        }
    }
}

// Attach event listeners to the document for Bootstrap modal events
document.addEventListener('show.bs.modal', onModalShow);
document.addEventListener('hide.bs.modal', onModalHide);

// Function to open the help modal
function openHelpModal() {
    var modalElement = document.getElementById('helpModal');
    if (!modalElement) {
        console.error('Help modal element not found');
        return;
    }
    var modal = new bootstrap.Modal(modalElement);
    modal.show();
}

// Function to check if the modal should be shown on the first visit for this route
function checkModal() {
    var pageId = getPageIdentifier();  // Get unique identifier for the current page
    if (!getCookie('dontShowModal_' + pageId)) {
        openHelpModal();  // Show modal if no cookie for this page
    }
}

// Function to attach event listener to the help button
function attachHelpButtonListener() {
    var helpButton = document.getElementById('helpButton');
    if (helpButton) {
        // Remove any existing event listener to prevent duplicates
        helpButton.removeEventListener('click', openHelpModal);
        helpButton.addEventListener('click', openHelpModal);
    }
}

// Trigger the functions when the page loads
window.onload = function() {
    attachHelpButtonListener();
    checkModal();
};

// Also trigger modal check and reattach event listeners whenever the route changes
window.onpopstate = function() {
    attachHelpButtonListener();
    checkModal();
};

// Function to download a file (unchanged)
function downloadFile(event, fileUrl) {
    event.preventDefault();

    fetch(fileUrl)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok. Status code: ' + response.status);
            }
            return response.blob();
        })
        .then(function(blob) {
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);

            // Extract the filename from the fileUrl
            var filename = fileUrl.substring(fileUrl.lastIndexOf('/') + 1);
            // Decode URI components if necessary
            filename = decodeURIComponent(filename);

            link.download = filename; // Use the extracted filename

            // Append the link to the body
            document.body.appendChild(link);

            // Trigger the download
            link.click();

            // Clean up and revoke the object URL
            setTimeout(function() {
                document.body.removeChild(link);
                window.URL.revokeObjectURL(link.href);
            }, 100);
        })
        .catch(function(error) {
            console.error('There was a problem with the download:', error);
            alert('Could not download the file: ' + error.message);
        });
}
