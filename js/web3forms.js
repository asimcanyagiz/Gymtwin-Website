/**
 * Gymtwin contact form: mailto handler.
 * Opens the visitor's email client addressed to the Gymtwin support inbox.
 * No backend and no third-party service (keeps messages going straight to us).
 */
(function () {
  "use strict";

  var SUPPORT_EMAIL = "apputopiacy@gmail.com";
  var form = document.getElementById("contactForm");
  if (!form) return;

  var statusDiv = document.getElementById("formStatus");
  function setStatus(msg, ok) {
    if (!statusDiv) return;
    statusDiv.textContent = msg;
    statusDiv.className = "form-status " + (ok ? "success" : "error");
    statusDiv.style.display = "block";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Honeypot: bots tick the hidden checkbox, so silently drop.
    var bot = form.querySelector('[name="botcheck"]');
    if (bot && bot.checked) return;

    var name = (form.querySelector('[name="name"]') || {}).value || "";
    var email = (form.querySelector('[name="email"]') || {}).value || "";
    var message = (form.querySelector('[name="message"]') || {}).value || "";

    if (!name.trim() || !email.trim() || !message.trim()) {
      setStatus("Please fill in your name, email, and message.", false);
      return;
    }

    var subject = "Gymtwin website message from " + name;
    var body = "Name: " + name + "\nEmail: " + email + "\n\n" + message;
    var href =
      "mailto:" + SUPPORT_EMAIL +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);

    window.location.href = href;
    setStatus("Opening your email app... If nothing happens, write to " + SUPPORT_EMAIL + ".", true);
  });
})();
