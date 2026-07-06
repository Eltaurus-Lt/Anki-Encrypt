// load answer check
check = sessionStorage.getItem("card::passCheck");

if (check === 'true') {
  window.typeans.classList.add('correct');
  window.typeans.placeholder="✅";
} else if (check === 'false') {
  window.typeans.classList.add('wrong');
  window.typeans.placeholder="❌";
}