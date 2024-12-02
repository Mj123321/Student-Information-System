// Function to open the Add Student modal
function openAddModal() {
    document.getElementById("studentModal").style.display = "block";
    document.getElementById("studentForm").action = "/add"; // Ensure form submits to the correct route
}

// Function to close the modal
function closeModal() {
    document.getElementById("studentModal").style.display = "none";
}

// Optional: Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById("studentModal");
    if (event.target === modal) {
        closeModal();
    }
};
