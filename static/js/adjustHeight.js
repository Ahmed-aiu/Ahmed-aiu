/**
 * Adjusts the height of the 'application' element to fit within the window height,
 * accounting for the heights of the heading and navbar elements.
 */
function adjustHeight() {
    // Calculate the height of the window, reduced slightly by 1% for margins or padding
    var windowHeight = window.innerHeight * 0.99;

    // Calculate the height percentages of the heading and navbar relative to the window height
    var headingHeightPercent = (document.getElementById('heading').offsetHeight / windowHeight) * 100;

    // Calculate the remaining height for the application element as a percentage
    var applicationHeightPercent = 100 - (headingHeightPercent) - 1;

    // Set the application element's height as a percentage
    document.getElementById('application').style.height = applicationHeightPercent + '%';
}
