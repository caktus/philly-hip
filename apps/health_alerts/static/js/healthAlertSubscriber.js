export default function() {
  const healthAlertSubscriberEl = document.querySelector(".health-alert-subscriber-modal");
  const mobileHeader = document.getElementById("mobile-header-hip");
  
  if (healthAlertSubscriberEl) {
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
    const closeBtn = document.querySelector("#health-alert-subscriber-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      document.body.classList.remove("modal-is-open-hip");
      if (mobileHeader) {
        mobileHeader.classList.add("is-sticky-hip");
      }
      window.location.href = this.dataset.href;
    });
  }
}