function Flip() { // flip to the back of the card
  if (!!window.pycmd) { // desktop
    pycmd("ans");
  } else if (!!window.showAnswer) { // AnkiDroid
    showAnswer();
  } else if (!!window.qa_box) { // AnkiWeb
    document.querySelector('.btn.btn-primary.btn-lg').click();
  }
}

// cross-platform typing
window.typeans.addEventListener('input', (ev) => {
  checkPassword();
});
window.typeans.addEventListener('keydown', (ev) => {
  if (event.key === "Enter") {
    Flip();
  }
});
if (!!window.qa_box) { // AnkiWeb
  setTimeout( () => {  // re-focus the typing field
    document.activeElement.blur();
    window.typeans.focus();
  }, 100);
}