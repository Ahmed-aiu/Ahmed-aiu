function initStyle() {
    const savedTheme = localStorage.getItem('theme');
    const savedThemeLabel = localStorage.getItem('themeLabel');
    const savedThemeSwitch = localStorage.getItem('themeSwitch') === 'true';
    const themeLink = document.getElementById('theme-link');
    const themeSwitch = document.getElementById('themeSwitch');
    const themeLabel = document.getElementById('themeLabel');

    themeSwitch.style.transition = 'none'; // Disable transition

    if (savedTheme === 'dark') {
        themeLink.setAttribute('href', 'static/css/styleSheetFEV_dark.css');
        themeSwitch.checked = true;
        themeLabel.textContent = savedThemeLabel || 'Dark Theme';
    } else {
        themeLink.setAttribute('href', 'static/css/styleSheetFEV.css');
        themeSwitch.checked = savedThemeSwitch;
        themeLabel.textContent = savedThemeLabel || 'Light Theme';
    }

    setTimeout(() => {
        themeSwitch.style.transition = ''; // Restore transition
    }, 0); // Set to 0 milliseconds
}
