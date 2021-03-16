import { openMobileModal, closeMobileModal } from "./common";

export default function() {
  navbarBurger();
  setUpMobileSearchModal();
  showMobileSearchModal();

  function navbarBurger() {
    // This button handles the show/hide functionality of sidebar menu
    const navbarBurger = document.querySelector("#navbar-burger");
    navbarBurger.addEventListener("click", function () {
      const dataTarget = this.dataset.target;
      const target = document.getElementById(dataTarget);
      if (target.classList.contains("is-hidden-touch")) {
        openMobileModal(target);
      } else {
        closeMobileModal(target);
      }
    });
  }

  function setUpMobileSearchModal() {
    /* Handles the show/hide functionality of the mobile search container

      - search id="search-mobile-btn" in header.html to view the button
      - view mobile_search_modal.html for the content that is being shown/hidden
    */
    const searchMobileBtn = document.querySelector("#search-mobile-btn");

    searchMobileBtn.addEventListener("click", function () {
      const dataTarget = this.dataset.target;
      const target = document.getElementById(dataTarget);
      if (target.classList.contains("is-hidden-touch")) {
        openMobileModal(target);
      } else {
        closeMobileModal(target);
      }
    });
  }

  function showMobileSearchModal() {
    // If we are on the search page, and on mobile/tablet widths, then we should automatically show the modal
    const isSearchPage = document.querySelector(".search-page-hip");
    const width = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)

    if (isSearchPage && width < 1024) {
      const searchModal = document.querySelector("#searchMobileContainer");
      openMobileModal(searchModal);
    }

  }
};
