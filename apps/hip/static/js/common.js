export function openMobileModal (target) {
  // target: element to open as a modal
  target.classList.remove("is-hidden-touch");
  document.body.classList.add('modal-is-open-hip')
};

export function closeMobileModal (target) {
  // target: element to open as a modal
  target.classList.add("is-hidden-touch");
  document.body.classList.remove('modal-is-open-hip')
};
