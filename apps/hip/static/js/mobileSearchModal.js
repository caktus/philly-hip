export default function() {
  closeMobileSearchModal();

  function closeMobileSearchModal () {
    /* Hides search modal on mobile when clicked
    */
    const closeBtn = document.querySelector(".mobile-search-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      const target = document.getElementById("searchMobileContainer");
      if (target.classList.contains("is-hidden-touch")) {
        target.classList.remove("is-hidden-touch");
      } else {
        target.classList.add("is-hidden-touch");
      }
    });
  }
};