document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("show-details-btn");
  var detailsSection = document.getElementById("details-section");

  if (!btn || !detailsSection) {
    return;
  }

  // Populate the details section with additional student information
  detailsSection.innerHTML =
    '<div class="info-grid">' +
    '<div class="info-group">' +
    '<span class="info-label">Semester:</span>' +
    '<span class="info-value">5th Trimester</span>' +
    '</div>' +
    '<div class="info-group">' +
    '<span class="info-label">Section:</span>' +
    '<span class="info-value">MCA DevOps</span>' +
    '</div>' +
    '<div class="info-group info-group-wide">' +
    '<span class="info-label">University:</span>' +
    '<span class="info-value">CHRIST (Deemed-to-be University)</span>' +
    '</div>' +
    '</div>';

  // Initially hide the details section
  detailsSection.hidden = true;

  // Set initial ARIA state on the button
  btn.setAttribute("aria-expanded", "false");
  btn.setAttribute("aria-controls", "details-section");

  // Toggle details visibility on button click
  btn.addEventListener("click", function () {
    var isHidden = detailsSection.hidden;

    detailsSection.hidden = !isHidden;
    btn.setAttribute("aria-expanded", String(isHidden));
    btn.textContent = isHidden ? "Hide Details" : "Show Details";
  });
});
