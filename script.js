// ==========================
// CONFIG
// ==========================
const VIDEO_MAP = {
  Gymbadi: "assets/gymbadi/video.mp4",
  Iora: "assets/iora/video.mp4",
};

let lastFocusedElement = null;

// ==========================
// VIDEO MODAL
// ==========================
function openVideoModal(projectName) {
  const modal = document.getElementById("video-modal");
  const modalContent = document.getElementById("video-modal-content");
  const titleEl = document.getElementById("modal-video-title");

  if (!modal || !modalContent || !titleEl) return;

  lastFocusedElement = document.activeElement;
  titleEl.textContent = projectName;

  const videoHost = modalContent.querySelector(".aspect-video");
  if (videoHost) {
    const src = VIDEO_MAP[projectName];

    if (!src) {
      videoHost.innerHTML = `<p class="text-white text-lg font-light">Video not set for ${projectName}</p>`;
    } else {
      videoHost.innerHTML = `
        <video controls autoplay playsinline class="w-full h-full object-contain bg-black">
          <source src="${src}" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      `;
    }
  }

  modal.classList.remove("hidden");
  modal.classList.add("flex");

  // Animate in
  requestAnimationFrame(() => {
    modal.classList.remove("opacity-0");
    modal.classList.add("opacity-100");
    modalContent.classList.remove("scale-95");
    modalContent.classList.add("scale-100");
  });

  document.body.style.overflow = "hidden";
}

function closeVideoModal() {
  const modal = document.getElementById("video-modal");
  const modalContent = document.getElementById("video-modal-content");
  if (!modal || !modalContent) return;

  // Animate out
  modal.classList.add("opacity-0");
  modal.classList.remove("opacity-100");
  modalContent.classList.add("scale-95");
  modalContent.classList.remove("scale-100");

  // Stop playback + remove video element to fully release it
  const video = modal.querySelector("video");
  if (video) {
    try {
      video.pause();
      video.removeAttribute("src");
      video.load();
    } catch (_) {}
    video.remove();
  }

  setTimeout(() => {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.style.overflow = "";

    if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
      lastFocusedElement.focus();
    }
  }, 200);
}

// Expose functions for inline onclick="..."
window.openVideoModal = openVideoModal;
window.closeVideoModal = closeVideoModal;

// ==========================
// INIT
// ==========================
document.addEventListener("DOMContentLoaded", () => {
  // ----- Mobile menu -----
  const btn = document.getElementById("mobile-menu-btn");
  const menu = document.getElementById("mobile-menu");

  const closeMenu = () => {
    if (!menu) return;
    menu.classList.add("hidden");
    menu.classList.remove("flex");
    menu.classList.add("opacity-0");
    menu.classList.remove("opacity-100");
    document.body.style.overflow = "";
  };

  if (btn && menu) {
    btn.addEventListener("click", () => {
      const isHidden = menu.classList.contains("hidden");
      if (isHidden) {
        menu.classList.remove("hidden");
        menu.classList.add("flex");
        menu.scrollTop = 0;
        requestAnimationFrame(() => {
          menu.classList.remove("opacity-0");
          menu.classList.add("opacity-100");
        });
        document.body.style.overflow = "hidden";
      } else {
        closeMenu();
      }
    });

    menu.querySelectorAll(".mobile-link").forEach((a) => {
      a.addEventListener("click", closeMenu);
    });
  }

  // ----- Sticky header styling on scroll -----
  const navbar = document.getElementById("navbar");
  if (navbar) {
    const applyNavbarStyle = () => {
      const scrolled = window.scrollY > 8;

      navbar.classList.toggle("bg-white/85", scrolled);
      navbar.classList.toggle("backdrop-blur", scrolled);
      navbar.classList.toggle("border-b", scrolled);
      navbar.classList.toggle("border-slate-100", scrolled);
      navbar.classList.toggle("shadow-sm", scrolled);

      // Keep padding consistent
      navbar.classList.toggle("py-4", scrolled);
      navbar.classList.toggle("py-6", !scrolled);
    };

    applyNavbarStyle();
    window.addEventListener("scroll", applyNavbarStyle, { passive: true });
  }

  // ----- Escape key closes modal -----
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeVideoModal();
  });
});