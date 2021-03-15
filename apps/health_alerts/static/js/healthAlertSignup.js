export default function() {
  const healthAlertSignUpEl = document.querySelector(".health-alerts-sign-up-modal");
  
  if (healthAlertSignUpEl) {
    document.body.classList.add("modal-is-open-hip");
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
    const closeBtn = document.querySelector("#health-alert-signup-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      document.body.classList.remove("modal-is-open-hip");
      window.location.href = this.dataset.href;
    });
  }
}