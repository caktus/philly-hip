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

  /*************************
   *  INTERNAL ALERTS FORM *
   *************************/

  const internalAlertsAmbulatoryOptionValue = "Ambulatory Health Services";
  const internalAlertsAmbulatoryFieldName = "Ambulatory Health Center";
  const internalAlertsAmbulatoryElementSelector = "#id_ambulatory_health_center"
  const internalAlertsDiseaseControlOptionValue = "Division of Disease Control"
  const internalAlertsDiseaseControlFieldName = "Disease Control Program"
  const internalAlertsDiseaseControlElementSelector = "#id_disease_control_program"
  const internalAlertsEnvironmentalOptionValue = "Environmental Health Services"
  const internalAlertsEnvironmentalFieldName = "EHS Program"
  const internalAlertsEnvironmentalElementSelector = "#id_ehs_program"

  function getInternalAlertsFieldNameForDivisionOption(option) {
    // Given an <option> for the "Division" field, return the field name for that option.
    return {
      [ internalAlertsAmbulatoryOptionValue ]: internalAlertsAmbulatoryFieldName,
      [ internalAlertsDiseaseControlOptionValue ]: internalAlertsDiseaseControlFieldName,
      [ internalAlertsEnvironmentalOptionValue ]: internalAlertsEnvironmentalFieldName,
    }[option.value]
  }

  function hideInternalAlertFormExtraFields() {
    // Hide the Ambulatory Health Center, EHS Program and Disease Control Program fields.
    document.querySelectorAll(".form-sections-hip").forEach(element => {
      // Loop through the .form-sections-hip elements (which contain each of the fields),
      // and hide each field that has a child matching any of the extra fields selectors.
      if (element.querySelector(internalAlertsAmbulatoryElementSelector)) {
        element.style.display = "none";
      } else if (element.querySelector(internalAlertsDiseaseControlElementSelector)) {
        element.style.display = "none";
      } else if (element.querySelector(internalAlertsEnvironmentalElementSelector)) {
        element.style.display = "none";
      }
    })
  }

  function showField(fieldName) {
    // Loop through the .form-sections-hip elements (which contain each of the fields).
    // If an element has a child that matches the selector for the fieldName,
    // then the element should become visible.
    document.querySelectorAll(".form-sections-hip").forEach(element => {
      // Loop through the .form-sections-hip elements (which contain each of the fields),
      // and show the field that matches the fieldName (if it exists).
      if (fieldName === internalAlertsAmbulatoryFieldName && element.querySelector(internalAlertsAmbulatoryElementSelector)) {
        element.style.display = "";
      } else if (fieldName === internalAlertsDiseaseControlFieldName && element.querySelector(internalAlertsDiseaseControlElementSelector)) {
        element.style.display = "";
      } else if (fieldName === internalAlertsEnvironmentalFieldName && element.querySelector(internalAlertsEnvironmentalElementSelector)) {
        element.style.display = "";
      }
    })
  }

  function hideInternalAlertFormExtraFieldsExcept(fieldName) {
    // Hide all of the extra fields for the internal alerts form, then show
    // the field for the fieldName.
    hideInternalAlertFormExtraFields();
    // Show the field for the fieldName.
    showField(fieldName)
  }

  const internalAlertsFormDivisionSelect = document.querySelector("#internal-alerts-subscriber-form #id_division");
  // Hide all of the extra fields on the internal alerts form, except the field
  // for the selected "Division" field option (if there is one).
  internalAlertsFormDivisionSelect.querySelectorAll("option").forEach(element => {
    if (element.selected === true) {
      const fieldName = getInternalAlertsFieldNameForDivisionOption(element);
      hideInternalAlertFormExtraFieldsExcept(fieldName);
    }
  })

  // Add an event listener to the "Division" field dropdown.
  // If a user selects the Ambulatory <option>, then the internalAlertsAmbulatoryFieldName field
  // should become visible.
  // If a user selects the Disease Control <option>, then the internalAlertsDiseaseControlFieldName field
  // should become visible.
  // If a user selects the Environmental <option>, then the internalAlertsEnvironmentalFieldName field
  // should become visible.
  internalAlertsFormDivisionSelect.addEventListener("change", (event) => {
    internalAlertsFormDivisionSelect.querySelectorAll("option").forEach(element => {
      if (element.selected === true) {
        const fieldName = getInternalAlertsFieldNameForDivisionOption(element);
        hideInternalAlertFormExtraFieldsExcept(fieldName);
      }
    })
  })
}
