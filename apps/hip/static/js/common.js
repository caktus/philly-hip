export function openMobileModal (target) {
  // target: element to open as a modal
  target.classList.remove("is-hidden-touch");
  document.body.classList.add('modal-is-open-hip')
  // un-stick the navbar
  const navbar = document.getElementById("mobile-navbar-hip");
  navbar.classList.remove("is-sticky-hip");
};

export function closeMobileModal (target) {
  // target: element representing the modal to close
  target.classList.add("is-hidden-touch");
  document.body.classList.remove('modal-is-open-hip')
  // re-stick the navbar
  const navbar = document.getElementById("mobile-navbar-hip");
  navbar.classList.add("is-sticky-hip");
};
