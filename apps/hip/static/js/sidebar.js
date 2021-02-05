export default function () {
  const sideNavLinks = document.querySelectorAll(".sidenav-link-scss");

  function removeIsActive() {
    /* Find the active sidebar element and remove the is-active-scss class
    */
    const isActiveEl = document.querySelector(".is-active-scss");
    isActiveEl.classList.remove("is-active-scss")
  }

  // Event Listener for when sidebar nav elements are clicked.
  sideNavLinks.forEach(sideNavLink => sideNavLink.addEventListener("click", function () {
    removeIsActive()
    // now make the clicked element display as being active
    this.classList.add("is-active-scss");
    // relocate the user
    window.location.href = this.dataset.href;
  }));
};
