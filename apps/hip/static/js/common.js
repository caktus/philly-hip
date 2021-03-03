export function openMobileModal (target) {
  // target: element to open as a modal
  target.classList.remove("is-hidden-touch");
  document.body.classList.add('modal-is-open-hip')
  // un-stick the header
  const header = document.getElementById("mobile-header-hip");
  header.classList.remove("is-sticky-hip");
};

export function closeMobileModal (target) {
  // target: element representing the modal to close
  target.classList.add("is-hidden-touch");
  document.body.classList.remove('modal-is-open-hip')
  // re-stick the header
  const header = document.getElementById("mobile-header-hip");
  header.classList.add("is-sticky-hip");
};
