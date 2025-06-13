let chooserListenerElements = []


function addPageTitleToLinkTitle() {
    setTimeout(() => {
        titleInput = this.closest('.w-panel__content').querySelector('input')
        pageTitle = this.parentElement.querySelector('.chooser__title').innerText
        titleInput.value = pageTitle
    }, 300)
    
}

const clearEventListeners = () => {
    for (let i = 0; i < chooserListenerElements.length ; i++) {
        chooserListenerElements[i].removeEventListener('change', addPageTitleToLinkTitle)
    }

    // Reset chooserListenerElements
    chooserListenerElements = []
}

const addChangeEventListenerToChoosers = () => {
    clearEventListeners()

    const pageChoosers = document.querySelectorAll('.page-chooser')
    pageChoosers.forEach((el, i) => {
        const chooserInput = el.nextElementSibling
        chooserInput.addEventListener('change', addPageTitleToLinkTitle);
        chooserListenerElements.push(el)
    })
}

document.addEventListener("DOMContentLoaded", function() {
    // Only call this javascript when editing a menu snippet
    // This code adds the page title to the link title when using the page chooser
    if (window.location.pathname.includes('snippets/hip/menu')) {
        // `(+) Add page link` button
        const addPageLinkButton = document.getElementById('id_page_links-ADD');

        addPageLinkButton.addEventListener('click', function() {
            addChangeEventListenerToChoosers()
        });

        // Call once on page load
        addChangeEventListenerToChoosers()
    }
});
