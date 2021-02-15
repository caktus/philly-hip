export default function () {
  /* Use IntersectionObserver to determine when a section of the page is within
   * the user's view; when it is, add a CSS class to its respective anchor tag.
   * Docs: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
   *       https://codepen.io/mishunov/pen/opeRdL
   */

  const pageSections = document.querySelectorAll("div.nav-heading-hip");
  const config = {};

  // Define the IntersectionObserver.
  let observer = new IntersectionObserver(function (entries, self) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        intersectionHandler(entry);
      }
    });
  }, config);

  // Observe each of the page pageSections.
  pageSections.forEach(section => {
    observer.observe(section);
  });

  function intersectionHandler(entry) {
    /* When an entry is being intersected, add the 'is-current-hip' CSS class to its
     * respective anchor tag (with the 'nav-title>a' CSS class). Remove the 'is-current-hip'
     * CSS class from other 'nav-title>a' elements.
     */

    const id = entry.target.id;
    const elementCurrentlyActive = document.querySelector(".nav-title a.is-current-hip");
    const elementBecomingActive = document.querySelector(".nav-title[data-ref=" + id + "] a");

    // Give the 'is-current-hip' CSS class from the nav title that is becoming non-active.
    if (elementCurrentlyActive) {
      elementCurrentlyActive.classList.remove("is-current-hip");
    }
    // Give the 'is-current-hip' CSS class to the nav title that is becoming active.
    if (elementBecomingActive) {
      elementBecomingActive.classList.add("is-current-hip");
    }
  }

  // smooth scroll to #targets
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();

      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
};
