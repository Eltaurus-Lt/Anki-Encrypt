// prevent ankiweb from immediately rating a card flipped by Enter
if (!!window.qa_box && !window.awRefocus) {
  const btnAreaL = document.getElementById("ansarea");
  window.awRefocus = new MutationObserver(() => {
    btnAreaL.querySelectorAll('[autofocus]').forEach(L => {
      L.removeAttribute('autofocus');
      L.blur();
      setTimeout(()=>{
        let AWrateButtons = window.ansarea?.querySelectorAll('.btn.btn-primary.btn-lg');
        if (AWrateButtons?.length !== 4) {AWrateButtons = null} // prevent focusing on a wrong screen
        if (check === 'true') {
          AWrateButtons?.[2].focus();
        } else if (check === 'false') {
          AWrateButtons?.[0].focus();
        }
      }, 0);
    });
  });
  window.awRefocus.observe(btnAreaL, { childList: true, subtree: true });
};