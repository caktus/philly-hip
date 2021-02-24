import { closeMobileModal } from "./common";

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

    // Activate the sidebar link matching the current path
    const currentPath = window.location.pathname;
    const sidebarEl = document.querySelector(`[data-href="${currentPath}"]`);
    if (sidebarEl) {
      removeIsActive()
      sidebarEl.classList.add("is-active-hip");
    }
  };

  function manageCloseButtonClicked () {
    /* Hides sidebar on mobile when clicked
    */
    const closeBtn = document.querySelector(".sidebar-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      const target = document.getElementById("sidebarContent");
      closeMobileModal(target);
    });
  }
};
