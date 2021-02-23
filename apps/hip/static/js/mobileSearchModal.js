import { closeMobileModal } from "./common";

export default function() {
  closeMobileSearchModal();

  function closeMobileSearchModal () {
    /* Hides search modal on mobile when clicked
    */
    const closeBtn = document.querySelector(".mobile-search-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      const target = document.getElementById("searchMobileContainer");
      closeMobileModal(target);
    });
  }
};
