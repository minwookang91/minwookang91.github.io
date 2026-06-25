
let allPublications = [];
let activeFilter = "all";
let query = "";

function normalize(text) {
  const temp = document.createElement("div");
  temp.innerHTML = text || "";
  return (temp.textContent || "").toLowerCase();
}

function renderPublications() {
  const list = document.getElementById("publication-list");
  const filtered = allPublications.filter(pub => {
    const matchesFilter = activeFilter === "all" || pub.type === activeFilter;
    const haystack = normalize([pub.title, pub.authors, pub.venue, pub.year, pub.type, pub.status].join(" "));
    return matchesFilter && haystack.includes(query);
  });

  document.getElementById("publication-count").textContent = filtered.length;
  if (!filtered.length) {
    list.innerHTML = '<div class="empty-state">No publications match this search.</div>';
    return;
  }

  let currentYear = null;
  let number = 0;
  list.innerHTML = filtered.map(pub => {
    number += 1;
    let yearHeading = "";
    if (pub.year !== currentYear) {
      currentYear = pub.year;
      yearHeading = `<div class="year-heading"><h2>${pub.year}</h2><div></div></div>`;
    }
    const abstractButton = pub.abstract
      ? `<button class="abstract-toggle" type="button" aria-expanded="false">ABS</button>`
      : "";
    const abstract = pub.abstract
      ? `<div class="abstract"><p>${pub.abstract}</p></div>`
      : "";
    return `${yearHeading}
      <article class="publication-item">
        <div class="pub-number">${String(number).padStart(2, "0")}</div>
        <div class="pub-body">
          <div class="pub-topline">
            <span class="pub-type">${pub.type}</span>
            ${pub.status ? `<span class="pub-status">${pub.status}</span>` : ""}
          </div>
          <h3>${pub.title}</h3>
          <div class="pub-authors">${pub.authors}</div>
          <div class="pub-venue">${pub.venue}, ${pub.year}</div>
          <div class="pub-actions">
            ${abstractButton}
            <a href="https://doi.org/${pub.doi}" target="_blank" rel="noopener">DOI</a>
          </div>
          ${abstract}
        </div>
      </article>`;
  }).join("");

  list.querySelectorAll(".abstract-toggle").forEach(button => {
    button.addEventListener("click", () => {
      const abstract = button.closest(".pub-body").querySelector(".abstract");
      const open = abstract.classList.toggle("open");
      button.setAttribute("aria-expanded", String(open));
      button.textContent = open ? "CLOSE" : "ABS";
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  allPublications = window.PUBLICATIONS || [];
  allPublications.sort((a, b) => b.year - a.year);
  renderPublications();

  document.getElementById("publication-search").addEventListener("input", event => {
    query = event.target.value.trim().toLowerCase();
    renderPublications();
  });

  document.querySelectorAll(".filter").forEach(button => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".filter").forEach(item => item.classList.remove("active"));
      button.classList.add("active");
      activeFilter = button.dataset.filter;
      renderPublications();
    });
  });
});
