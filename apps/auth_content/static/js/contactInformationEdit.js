export default function() {
  const contactInformationEditModal = document.querySelector(".contact-information-edit-modal");
  const mobileHeader = document.getElementById("mobile-header-hip");
  const sidebar = document.querySelector("#sidebarContent");
  
  if (contactInformationEditModal) {
    document.body.classList.add("modal-is-open-hip");
    sidebar.classList.add("is-hidden-desktop");
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
    const closeBtn = document.querySelector("#contact-information-edit-close-btn-hip");
    closeBtn.addEventListener("click", function () {
      window.location.href = this.dataset.href;
    });
  }
}