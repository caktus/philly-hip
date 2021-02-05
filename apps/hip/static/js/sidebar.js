export default function () {
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
