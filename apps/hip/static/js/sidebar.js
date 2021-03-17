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
      if (isActiveEl) {
        isActiveEl.classList.remove("is-active-hip");
      }
    }

    function getParentSidebarLink (currentPath) {
      /* Use Breadcrumb navigation to determine which SideBarLink is active

      This function's logic is based on the assumption that sections that
      have a page depth of greater than 1 will use breadcrumb navigation
      and  the first <a> of the breadcrumb will have an href that matches
      one of the sidebar data-href attributes.
      */
      const breadcrumbUL = document.querySelector("#breadcrumb-ul-hip");
      if (breadcrumbUL) {
        const parentBreadCrumb = breadcrumbUL.getElementsByTagName("li")[0];
        const sideBarLink = parentBreadCrumb.getElementsByTagName("a")[0];
        const sideBarLinkHref = sideBarLink.getAttribute("href");
        if (currentPath.includes(sideBarLinkHref)) {
          const actualSidebarLink = document.querySelector(`[data-href="${sideBarLinkHref}"]`);
          return actualSidebarLink;
        }
      }
      return null
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
    const parentSideBarEl = getParentSidebarLink(currentPath);
    if (sidebarEl) {
      removeIsActive();
      sidebarEl.classList.add("is-active-hip");
    } else if (!sidebarEl && parentSideBarEl)  {
      removeIsActive();
      parentSideBarEl.classList.add("is-active-hip");
    } else {
      removeIsActive();
    }
  };

  function manageCloseButtonClicked () {
    /* Hides sidebar on mobile when clicked
    */
    const closeBtn = document.querySelector(".sidebar-close-btn-hip");
    closeBtn && closeBtn.addEventListener("click", function () {
      const target = document.getElementById("sidebarContent");
      closeMobileModal(target);
    });
  }
};
