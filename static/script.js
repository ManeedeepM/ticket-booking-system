document.addEventListener("DOMContentLoaded", () => {
  console.log("Ticket Booking System loaded.");

  const registerForm = document.querySelector("form[action='/register']");
  const loginForm = document.querySelector("form[action='/login']");
  const bookForm = document.querySelector("form[action='/book']");

  if (registerForm) {
    registerForm.addEventListener("submit", (e) => {
      const password = registerForm.querySelector("input[name='password']").value;
      if (password.length < 6) {
        alert("Password should be at least 6 characters long.");
        e.preventDefault();
      }
    });
  }

  if (bookForm) {
    bookForm.addEventListener("submit", (e) => {
      const tickets = parseInt(bookForm.querySelector("input[name='tickets']").value);
      if (isNaN(tickets) || tickets < 1) {
        alert("Please enter a valid number of tickets.");
        e.preventDefault();
      }
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", () => {
      console.log("Attempting login...");
    });
  }
});
