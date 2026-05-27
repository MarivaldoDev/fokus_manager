document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("confirm-modal");
  if (!modal) {
    return;
  }

  const messageElement = modal.querySelector("[data-confirm-message], #confirm-modal-message");
  const acceptButton = modal.querySelector("[data-confirm-accept]");
  const closeButtons = modal.querySelectorAll("[data-confirm-close]");
  const dialog = modal.querySelector(".confirm-modal__dialog");
  let activeForm = null;

  const closeModal = () => {
    modal.hidden = true;
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("confirm-modal-open");
    activeForm = null;
  };

  const openModal = (form) => {
    activeForm = form;
    messageElement.textContent = form.dataset.confirmMessage || "Tem certeza que deseja continuar?";
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("confirm-modal-open");
    dialog.focus();
  };

  document.querySelectorAll("form[data-confirm-message]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (form.dataset.confirmApproved === "true") {
        delete form.dataset.confirmApproved;
        return;
      }

      event.preventDefault();
      openModal(form);
    });
  });

  acceptButton.addEventListener("click", () => {
    if (!activeForm) {
      return;
    }

    activeForm.dataset.confirmApproved = "true";
    const form = activeForm;
    closeModal();
    form.submit();
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", closeModal);
  });

  modal.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.hidden) {
      closeModal();
    }
  });
});