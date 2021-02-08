export default function () {
  /* Use IntersectionObserver to determine when a section of the page is within
   * the user's view; when it is, add a CSS class to its respective nav title.
   */

  const pageSections = document.querySelectorAll("section.page-section-hip");
  const config = {
    threshold: [0, 0.25, 0.5, 0.75, 1]
  };

  // Define the IntersectionObserver.
  let observer = new IntersectionObserver(function (entries, self) {
    entries.forEach(entry => {
      if (entry.isIntersecting && entry.intersectionRect.top > 0) {
        intersectionHandler(entry);
      }
    });
  }, config);

  // Observe each of the page pageSections.
  pageSections.forEach(section => {
    observer.observe(section);
  });

  function intersectionHandler(entry) {
    /* When an entry is being intersected, add the 'is-active' CSS class to its
     * respective nav title (with the 'nav-title' CSS class). Remove the 'is-active'
     * CSS class from other 'nav-title' elements.
     */

    const id = entry.target.id;
    const elementCurrentlyActive = document.querySelector(".nav-title.is-active");
    const elementBecomingActive = document.querySelector(".nav-title[data-ref=" + id + "]");

    // Give the 'is-active' CSS class from the nav title that is becoming non-active.
    if (elementCurrentlyActive) {
      elementCurrentlyActive.classList.remove("is-active");
    }
    // Give the 'is-active' CSS class to the nav title that is becoming active.
    if (elementBecomingActive) {
      elementBecomingActive.classList.add("is-active");
    }
  }
};
