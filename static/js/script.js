document.getElementById("book-form").addEventListener("submit", function (e) {
    e.preventDefault();

    // Get form values
    const title = document.getElementById("title").value;
    const author = document.getElementById("author").value;
    const isbn = document.getElementById("isbn").value;
    const issueDate = new Date(document.getElementById("issue-date").value);
    const returnDate = new Date(document.getElementById("return-date").value);

    // Calculate fine
    const timeDifference = returnDate - issueDate; // Difference in milliseconds
    const dayDifference = timeDifference / (1000 * 60 * 60 * 24); // Convert to days
    let fine = 0;
    if (dayDifference > 10) {
        fine = (dayDifference - 10) * 10; // ₹10 fine for each day after 10 days
    }

    // Add book to table
    const table = document.getElementById("book-list");
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${title}</td>
      <td>${author}</td>
      <td>${isbn}</td>
      <td>${issueDate.toISOString().split('T')[0]}</td>
      <td>${returnDate.toISOString().split('T')[0]}</td>
      <td>₹${fine}</td> <!-- Display the calculated fine -->
      <td><button class="delete-button">Delete</button></td>
    `;

    table.appendChild(row);

    // Clear form
    document.getElementById("book-form").reset();

    // Delete book
    row.querySelector(".delete-button").addEventListener("click", function () {
        row.remove();
    });
});

document.getElementById("return-date").addEventListener("change", function () {
    const issueDate = new Date(document.getElementById("issue-date").value);
    const returnDate = new Date(this.value);

    // Calculate fine for preview
    const timeDifference = returnDate - issueDate;
    const dayDifference = timeDifference / (1000 * 60 * 60 * 24);
    let fine = 0;
    if (dayDifference > 10) {
        fine = (dayDifference - 10) * 10; // ₹10 fine for each day after 10 days
    }

    // Display fine message
    const fineMessage = document.getElementById("fine-message");
    if (fine > 0) {
        fineMessage.textContent = `Fine: ₹${fine} (for exceeding 10 days)`;
        fineMessage.style.color = "red";
    } else {
        fineMessage.textContent = "";
    }
});
