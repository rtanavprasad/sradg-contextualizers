document.addEventListener("DOMContentLoaded", function () {
    // Function to toggle dropdown visibility
    const dropdownBtns = document.querySelectorAll(".dropdown-btn");

    dropdownBtns.forEach((btn) => {
        btn.addEventListener("click", function (e) {
            e.stopPropagation(); // Prevent click from propagating
            closeAllDropdowns(); // Close other dropdowns
            const dropdownContent = this.nextElementSibling;
            dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
        });
    });

    // Close all dropdowns when clicking outside
    document.addEventListener("click", function () {
        closeAllDropdowns();
    });

    function closeAllDropdowns() {
        const dropdownContents = document.querySelectorAll(".dropdown-content");
        dropdownContents.forEach((content) => {
            content.style.display = "none";
        });
    }

    // Logic to handle checkbox selections and display selected items
    const allDropdowns = document.querySelectorAll(".dropdown-checkbox");

    allDropdowns.forEach((dropdown) => {
        const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]');
        const selectedContainer = dropdown.querySelector('.selected-columns');

        checkboxes.forEach((checkbox) => {
            checkbox.addEventListener("change", function () {
                const selectedValues = [];
                checkboxes.forEach((checkbox) => {
                    if (checkbox.checked) {
                        selectedValues.push(checkbox.value);
                    }
                });

                // Display selected items
                selectedContainer.innerHTML = selectedValues
                    .map((value) => `<span>${value}</span>`)
                    .join("");
            });
        });
    });

    // Analyze Button Logic to Retrieve Selected Values
    const analyzeBtns = document.querySelectorAll(".box-section button");
    analyzeBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
            const selectedValues = [];
            const selectedColumnsContainers = this.parentElement.querySelectorAll(".selected-columns");
            selectedColumnsContainers.forEach((container) => {
                const selectedItems = container.querySelectorAll('span');
                selectedItems.forEach((item) => {
                    selectedValues.push(item.textContent);
                });
            });
            console.log("Selected Values:", selectedValues); // Display selected values
            alert(`Selected Columns: ${selectedValues.join(", ")}`);
        });
    });
});
