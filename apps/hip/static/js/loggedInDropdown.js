export default function () {
  const loggedInBtn = document.querySelector("#logged-in-dropdown-btn");
  if (loggedInBtn) {
    manageDropdownIsActiveClickEvent(loggedInBtn);
  }
  function manageDropdownIsActiveClickEvent (btn) {
    const dropdown = document.querySelector("#logged-in-dropdown");
  
    btn.addEventListener("click", function () {
      const dropdownIsActive = dropdown.classList.contains("is-active");
      console.log(dropdownIsActive)
      if (dropdownIsActive) {
        dropdown.classList.remove("is-active");
      } else {
        dropdown.classList.add("is-active");
      }
    });

    // if user clicks outside of the dropdown, close the dropdown
    document.body.addEventListener("click", function(event) {
      if (!dropdown.contains(event.target)) {
        dropdown.classList.remove("is-active");
      }
    });
  };
}