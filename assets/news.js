// The news table is rendered at build time, with the older rows shipped hidden.
// This only unhides them, so the page works fine without JS.
const button = document.getElementById("news_load_btn");
const table = document.getElementById("news-table");

if (button && table) {
  const step = Number(button.dataset.step) || 5;
  button.hidden = false;

  button.addEventListener("click", () => {
    const hidden = [...table.querySelectorAll("tr[hidden]")];
    hidden.slice(0, step).forEach((row) => (row.hidden = false));
    if (hidden.length <= step) button.remove();
  });
}
