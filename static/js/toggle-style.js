function toggleStyle() {
    const themeLink = document.getElementById('theme-link');
    const themeSwitch = document.getElementById('themeSwitch');
    const themeLabel = document.getElementById('themeLabel');
    if (themeLink.getAttribute('href') === 'static/css/styleSheetFEV.css') {
        themeLink.setAttribute('href', 'static/css/styleSheetFEV_dark.css');
        setCookie('theme', 'dark', 30);
        themeSwitch.checked = true;
        themeLabel.textContent = 'Dark Theme';
        localStorage.setItem('theme', 'dark');
    } else {
        themeLink.setAttribute('href', 'static/css/styleSheetFEV.css');
        setCookie('theme', 'light', 30);
        themeSwitch.checked = false;
        themeLabel.textContent = 'Light Theme';
        localStorage.setItem('theme', 'light');
    }
    localStorage.setItem('themeLabel', themeLabel.textContent);
    localStorage.setItem('themeSwitch', themeSwitch.checked);
}
