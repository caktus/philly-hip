export default function() {
  const healthAlertSignUpEl = document.querySelector(".health-alerts-sign-up-modal");
  
  if (healthAlertSignUpEl) {
    styleInputElements();
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
}