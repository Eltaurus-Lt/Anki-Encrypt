// answer check
correctHash = window.ans.content.textContent.slice(-64);
saltString = window.ans.content.textContent.slice(0, -64);
// saving typed answer
function checkPassword() {
  sessionStorage.removeItem("card::passCheck");
  sha256withSalt(window.typeans.value, saltString).then((typedHash) => {
    sessionStorage.setItem("card::passCheck", typedHash === correctHash);
  });
}

sessionStorage.setItem("card::passCheck", false);