import { closeMobileModal } from "./common";

export default function() {
  closeMobileSearchModal();

  function closeMobileSearchModal () {
    /* Hides search modal on mobile when clicked
    */
    const closeBtn = document.querySelector(".mobile-search-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      // if the user has clicked around the search results, we can't just close the
      // modal. we also need to redirect them to the page they were on before starting
      // to search
      const urlParams = new URLSearchParams(window.location.search);
      const initialUrl = urlParams.get('initial_url');
      if (initialUrl) {
        window.location.href = initialUrl;
      } else {
        // they haven't clicked around the search results, so we can just close the modal
        const target = document.getElementById("searchMobileContainer");
        closeMobileModal(target);
      }
    });

  }
};
