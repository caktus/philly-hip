export function mobileModalOpen (target) {
  target.classList.remove("is-hidden-touch");
  document.body.classList.add('modal-is-open-hip')
};

export function mobileModalClosed (target) {
  target.classList.add("is-hidden-touch");
  document.body.classList.remove('modal-is-open-hip')
};
