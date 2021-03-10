export default function() {
  const hasHealthAlerts = document.querySelector('.alert-table-hip');
  const selectPriorityEl = document.querySelector('.select-priority');
  const selectConditionEl = document.querySelector('.select-condition');
  const alertsMissingEl = document.querySelector(".alerts-missing-hip");
  const allRows = document.querySelectorAll("[data-priority]");
  const isHealthAlertsPage = selectPriorityEl && selectConditionEl;
  const isDiseaseAndConditionDetailPage = hasHealthAlerts && !isHealthAlertsPage

  if (isHealthAlertsPage) {
    // do an initial render on page load to stripe the rows properly
    const initialRows = getInitialRows();
    renderRows(initialRows);

    // add a change event handler for each of the select dropdowns
    [selectPriorityEl, selectConditionEl].forEach(el => {
      el.addEventListener('change', (event) => {
        const selectedPriority = selectPriorityEl.value;
        const selectedCondition = selectConditionEl.value;

        let matchString = "";
        if (selectedPriority !== 'All') {
          matchString = `[data-priority~="${selectedPriority}"]`;
        }
        if (selectedCondition !== 'All') {
          matchString += `[data-condition~="${selectedCondition}"]`
        }
        if (matchString === ""){
          renderRows(allRows);
        } else {
          const rowsToShow = document.querySelectorAll(matchString);
          renderRows(rowsToShow);
        }
      })
    })
  }
  if (isDiseaseAndConditionDetailPage) {
    // On the disease/condition page, we have a health alerts table, but we don't want
    // to do any filtering (and especially we don't want to hide the right sidebar links
    // because they are unrelated to the health alerts on this page). We just want to
    // filter the rows (which shows the 'no health alerts' row, if needed, andd then
    // restripe the rows.
    filterRows(allRows);
    restripeRows(allRows);
  }

  function getInitialRows(){
    // check the query param to see if we should be filtering on page load
    const urlParams = new URLSearchParams(window.location.search);
    const initialCondition = urlParams.get('condition')
    if (initialCondition) {
      // change the select dropdown to show this condition
      selectConditionEl.value = initialCondition;
      return document.querySelectorAll(`[data-condition~="${initialCondition}"]`);
    } else {
      return allRows;
    }
  }

  function renderRows(rows) {
    // convenience function to do all the things we need to do to render the rows properly
    filterRows(rows);
    restripeRows(rows);
    filterRightSideLinks(rows);
  }

  function filterRows(rowsToShow) {
    // hide all the rows
    allRows.forEach(row => row.hidden = true);
    // show just the rows the user wants to see
    rowsToShow.forEach(row => row.hidden = false);
    if (rowsToShow.length === 0) {
      // if all rows are hidden, then show our special "no alerts found" row
      alertsMissingEl.hidden = false;
    } else {
      alertsMissingEl.hidden = true;
    }
  }

  function restripeRows(rows) {
    const greyClass = "row-bg-grey-hip";
    const whiteClass = "row-bg-white-hip";
    let currentClass = whiteClass;
    let nextClass = greyClass;

    rows.forEach(row => {
      if (row.dataset.year !== undefined) {
        // Only the year header row has a `data-year` attribute, so this must be a new
        // year. Therefore, restart the colors, starting at white
        currentClass = whiteClass;
        nextClass = greyClass;
      } else {
        // swap the colors
        [currentClass, nextClass] = [nextClass, currentClass];
      }
      row.classList.add(currentClass);
      row.classList.remove(nextClass);
    });
  }

  function filterRightSideLinks(rows){
    // given the list of active rows, make sure only the right side links referring to
    // those years are shown
    const allRightSideLinks = document.querySelectorAll("[data-ref]");
    // hide all the right side links
    allRightSideLinks.forEach(row => row.hidden=true);
    rows.forEach(row => {
      // find all of the "year" values and unhide those rightsidelinks
      if (row.dataset.year !== undefined) {
        let rightSideLink = document.querySelector(`[data-ref=section-${row.dataset.year}]`);
        rightSideLink.hidden = false;
      }
    });
  }
};
