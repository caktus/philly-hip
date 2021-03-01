export default function() {
  const selectElement = document.querySelector('.select-priority');
  const alertsMissingEl = document.querySelector(".alerts-missing-hip");

  if (selectElement) {
    // add a handler for the change event for the priority select dropdown
    selectElement.addEventListener('change', (event) => {
      const selectedPriority = event.target.value;
      const allRows = document.querySelectorAll("[data-priority]");
      // we want to show any row that has the selectedPriority
      let rowsToShow = document.querySelectorAll(`[data-priority~="${selectedPriority}"]`);
      if (selectedPriority === 'All') {
        // show all rows again
        rowsToShow = allRows;
      }
      // filter the rows, restripe them, and then filter the right side links
      filterRows(rowsToShow, allRows);
      restripeRows(rowsToShow);
      filterRightSideLinks(rowsToShow);
    })
  }

  function filterRows(rowsToShow, allRows) {
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
