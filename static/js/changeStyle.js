function reStyle() {
    let idxStyleSheet = getCookie("ActiveStyleSheet");
    if (idxStyleSheet == 'FEV' || idxStyleSheet == '') {
        document.styleSheets[1].disabled = true; // deactivate FEV
        document.styleSheets[2].disabled = false; // activate TME

        // set cookie
        setCookie("ActiveStyleSheet", "TME", 7);
    } else if (idxStyleSheet == 'TME') {
        document.styleSheets[1].disabled = false; // activate FEV
        document.styleSheets[2].disabled = true; // deactivate TME

        // set cookie
        setCookie("ActiveStyleSheet", "FEV", 7)
    }
}

function initStyle() {
    // set correct CCS
    let idxStyleSheet = getCookie("ActiveStyleSheet");
    if (idxStyleSheet == 'FEV' || idxStyleSheet == '') {
        document.styleSheets[1].disabled = false; // deactivate FEV
        document.styleSheets[2].disabled = true; // activate TME

        // set cookie
        setCookie("ActiveStyleSheet", "FEV", 7);
    } else if (idxStyleSheet == 'TME') {
        document.styleSheets[1].disabled = true; // activate FEV
        document.styleSheets[2].disabled = false; // deactivate TME
    }
}

// const documentHeight = () => {
//     const doc = document.documentElement
//     doc.style.setProperty('--unit-100vh', `${window.innerHeight}px`)
// }
// window.addEventListener('resize', documentHeight);
// window.addEventListener('DOMContentLoaded', documentHeight);
// documentHeight();