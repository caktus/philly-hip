export default function () {
  const closeBtnArray = Array.from(document.querySelectorAll(".health-alert-close-btn-hip"));
  if (closeBtnArray.length) {
    closeBtnClicked(closeBtnArray);
  }

  function closeBtnClicked(elArray) {
    for (const el of elArray) {
      el.addEventListener("click", function() {
        this.parentElement.parentElement.classList.add("is-hidden");
      });
    }
  }
}