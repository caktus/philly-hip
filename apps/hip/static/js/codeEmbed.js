export default function () {
  const mobileMediaQuery = window.matchMedia("(max-width: 768px)");
  const embedBlocks = Array.from(document.querySelectorAll(".js-code-embed-hip"));

  if (!embedBlocks.length) {
    return;
  }

  const dismissHint = function (block) {
    block.classList.add("code-embed-hint-dismissed-hip");
  };

  embedBlocks.forEach(function (block) {
    const scrollArea = block.querySelector(".js-code-embed-scroll-hip");
    if (!scrollArea) {
      return;
    }

    const hideHintOnInteraction = function () {
      if (!mobileMediaQuery.matches) {
        return;
      }
      dismissHint(block);
    };

    scrollArea.addEventListener("touchstart", hideHintOnInteraction, { passive: true });
    scrollArea.addEventListener("pointerdown", hideHintOnInteraction, { passive: true });
    scrollArea.addEventListener("scroll", hideHintOnInteraction, { passive: true });

    const iframe = scrollArea.querySelector("iframe");
    if (iframe) {
      iframe.addEventListener("load", function () {
        iframe.style.touchAction = "auto";
      });
    }
  });
}
