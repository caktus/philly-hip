export default function() {
  navbarBurger();
  showHideMobileSearchModal();

  function navbarBurger() {
    // This button handles the show/hide functionality of sidebar menu
    const navbarBurger = document.querySelector("#navbar-burger");
    navbarBurger.addEventListener("click", function () {
      const dataTarget = this.dataset.target;
      const target = document.getElementById(dataTarget);
      if (target.classList.contains("is-hidden-touch")) {
        target.classList.remove("is-hidden-touch");
      } else {
        target.classList.add("is-hidden-touch");
      }
    });
  }

  function showHideMobileSearchModal() {
    /* Handles the show/hide functionality of the mobile search container

      - search id="search-mobile-btn" in header.html to view the button
      - view mobile_search_modal.html for the content that is being shown/hidden
    */
    const searchMobileBtn = document.querySelector("#search-mobile-btn");
    
    searchMobileBtn.addEventListener("click", function () {
      const dataTarget = this.dataset.target;
      const target = document.getElementById(dataTarget);
      if (target.classList.contains("is-hidden-touch")) {
        target.classList.remove("is-hidden-touch");
        document.body.classList.add('modal-is-open-hip')
      } else {
        target.classList.add("is-hidden-touch");
        document.body.classList.remove('modal-is-open-hip')
      }
    });
  }
};
