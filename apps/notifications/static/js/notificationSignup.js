export default function() {
  const notificationSubscriberEl = document.querySelector(".notification-signup-modal");
  const mobileHeader = document.getElementById("mobile-header-hip");

  if (notificationSubscriberEl) {
    document.body.classList.add("modal-is-open-hip");
    if (mobileHeader) {
      mobileHeader.classList.remove("is-sticky-hip");
    }
    styleInputElements();
    closeBtnClicked();
  }

  function styleInputElements() {
    const formSections = document.querySelectorAll(".form-sections-hip");
    for (const section of formSections) {
      const inputs = Array.from(section.getElementsByTagName("input"));
      if (inputs.length) {
        for (const input of inputs) {
          input.classList.add("input");
          input.classList.add("is-small");
        }
      }
    }
  };

  function closeBtnClicked() {
    const closeBtn = document.querySelector("#notification-signup-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      window.location.href = this.dataset.href;
    });
  }
}
