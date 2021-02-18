export default function () {
  manageSideBarLinks();
  manageCloseButtonClicked();

  function manageSideBarLinks () {
    const sideNavLinks = document.querySelectorAll(".sidenav-link-hip");

    function removeIsActive() {
      /* Find the active sidebar element and remove the is-active-hip class
      */
      const isActiveEl = document.querySelector(".is-active-hip");
      isActiveEl.classList.remove("is-active-hip")
    }

    // Event Listener for when sidebar nav elements are clicked.
    sideNavLinks.forEach(sideNavLink => sideNavLink.addEventListener("click", function () {
      removeIsActive()
      // now make the clicked element display as being active
      this.classList.add("is-active-hip");
      // relocate the user
      window.location.href = this.dataset.href;
    }));
  };

  function manageCloseButtonClicked () {
    /* Hides sidebar on mobile when clicked
    */
    const closeBtn = document.querySelector(".sidebar-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      const target = document.getElementById("sidebarContent");
      if (target.classList.contains("is-hidden-touch")) {
        target.classList.remove("is-hidden-touch");
      } else {
        target.classList.add("is-hidden-touch");
      }
    });
  }
};
