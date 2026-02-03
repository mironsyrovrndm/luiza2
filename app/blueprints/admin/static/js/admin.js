const setupRepeatableSection = (section) => {
  const addButton = section.querySelector("[data-add-item]");
  const list = section.querySelector(".repeatable__list");
  if (!addButton || !list) {
    return;
  }

  const createItem = () => {
    const template = list.querySelector("[data-repeatable-template]");
    let source = template;
    if (template && template.tagName === "TEMPLATE") {
      source = template.content.firstElementChild;
    }
    if (!source) {
      source = list.querySelector("[data-repeatable-item]");
    }
    if (!source) {
      return null;
    }
    const clone = source.cloneNode(true);
    clone.removeAttribute("data-repeatable-template");
    clone.classList.remove("is-template");
    clone.querySelectorAll("input, textarea").forEach((field) => {
      field.value = "";
    });
    return clone;
  };

  addButton.addEventListener("click", () => {
    const item = createItem();
    if (item) {
      list.appendChild(item);
    }
  });

  list.addEventListener("click", (event) => {
    const button = event.target.closest("[data-remove-item]");
    if (!button) {
      return;
    }
    const items = list.querySelectorAll("[data-repeatable-item]");
    if (items.length <= 1) {
      return;
    }
    const item = button.closest("[data-repeatable-item]");
    if (item) {
      item.remove();
    }
  });
};

document.querySelectorAll("[data-repeatable]").forEach((section) => {
  setupRepeatableSection(section);
});

const adminScrollKey = "admin-scroll-position";

document.addEventListener("click", (event) => {
  const toggle = event.target.closest("[data-record-toggle]");
  if (!toggle) {
    return;
  }
  const card = toggle.closest(".record-card");
  if (card) {
    card.classList.toggle("is-open");
  }
});

document.addEventListener("submit", (event) => {
  const form = event.target.closest("form");
  if (form) {
    sessionStorage.setItem(adminScrollKey, String(window.scrollY));
  }
});

window.addEventListener("load", () => {
  const stored = sessionStorage.getItem(adminScrollKey);
  if (stored) {
    const position = Number(stored);
    if (!Number.isNaN(position)) {
      window.scrollTo({ top: position });
    }
    sessionStorage.removeItem(adminScrollKey);
  }
});
