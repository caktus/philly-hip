import { addClickEventListenerBasedOnClassName } from "./common";

export default function () {
  /* Use IntersectionObserver to determine when a section of the page is within
   * the user's view; when it is, add a CSS class to its respective anchor tag.
   * Docs: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
   *       https://codepen.io/mishunov/pen/opeRdL
   */

  addClickEventListenerBasedOnClassName("right-scroll-link-hip", function (element) {
    // const elementCurrentlyActive = document.querySelector(".nav-title a.is-current-hip");
    // elementCurrentlyActive.classList.remove("is-current-hip");
    const elementCurrentlyActive = document.querySelector(".nav-title a.is-current-hip");
    const rightScrollNavContainer = document.querySelector(".right-scroll-container-hip");
    rightScrollNavContainer.setAttribute("isClicked", true);
    if (elementCurrentlyActive) {
      elementCurrentlyActive.classList.remove("is-current-hip");
    }
    element.classList.add("is-current-hip");
  });

  let pageSections = Array.from(document.querySelectorAll("div.nav-heading-hip"));

  if (pageSections.length) {
    const lastSection = pageSections.pop();
    const options = {
      // shrink root element that we're monitoring by 80% from the bottom so that we
      // monitor when elements intersect the top 20% of the page
      rootMargin: "0% 0% -80% 0%"
    };
    const lastSectionOptions = {
      // since the last section might be short, its header may never get to the top 20% of
      // the page, so we'll add a second observer that only observes whether the last
      // section intersects the top 50% of the page
      rootMargin: "0% 0% -50% 0%"
    };

    // Define the IntersectionObservers
    let observer = new IntersectionObserver(function (entries, self) {
      // main observer that observes all but the last section
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          intersectionHandler(entry);
        }
      });
    }, options);

    let lastSectionObserver = new IntersectionObserver(function (entries, self) {
      // observer for the last section
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          intersectionHandler(entry);
        }
      });
    }, lastSectionOptions);

    // Observe each of the pageSections (except the last one)
    pageSections.forEach(section => {
      observer.observe(section);
    });
    // Observe the last section
    lastSectionObserver.observe(lastSection);

    function intersectionHandler(entry) {
      /* When an entry is being intersected, add the 'is-current-hip' CSS class to its
      * respective anchor tag (with the 'nav-title>a' CSS class). Remove the 'is-current-hip'
      * CSS class from other 'nav-title>a' elements.
      */
      const rightScrollNavContainer = document.querySelector(".right-scroll-container-hip");
      const rightScrollLinkClicked = rightScrollNavContainer.getAttribute("isClicked");
      console.log(rightScrollLinkClicked);
      if (!rightScrollLinkClicked) {
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
      rightScrollNavContainer.setAttribute("isClicked", false);
      console.log(rightScrollLinkClicked);
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
  }
};
