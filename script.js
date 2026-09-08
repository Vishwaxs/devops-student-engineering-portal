document.addEventListener("DOMContentLoaded", function () {
  const showDetailsButton = document.getElementById("show-details-btn");

  if (showDetailsButton) {
    showDetailsButton.addEventListener("click", function () {
      console.log("Show Details button clicked. Interactive behavior reserved for Student 3.");
    });
  }
});
