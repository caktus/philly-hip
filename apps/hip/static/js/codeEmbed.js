export default function () {
  const embedBlocks = Array.from(document.querySelectorAll(".js-code-embed-hip"));

  if (!embedBlocks.length) {
    return;
  }

  const firstBlockStyle = window.getComputedStyle(embedBlocks[0]);
  const mobileBreakpoint =
    firstBlockStyle.getPropertyValue("--code-embed-mobile-breakpoint-hip").trim() || "768px";
  const landscapeHeightBreakpoint =
    firstBlockStyle.getPropertyValue("--code-embed-landscape-height-breakpoint-hip").trim() || "500px";
  const mobileMediaQuery = window.matchMedia(`(max-width: ${mobileBreakpoint})`);
  const landscapeMediaQuery = window.matchMedia(`(orientation: landscape) and (max-height: ${landscapeHeightBreakpoint})`);

  const dismissHint = function (block) {
    block.classList.add("code-embed-hint-dismissed-hip");
  };

  const getIntrinsicContentWidth = function (content) {
    let widest = content.scrollWidth;

    const iframes = content.querySelectorAll("iframe");
    iframes.forEach(function (iframe) {
      const iframeWidth = Number.parseFloat(iframe.getAttribute("width"));
      if (Number.isFinite(iframeWidth) && iframeWidth > 0) {
        iframe.style.width = `${iframeWidth}px`;
        widest = Math.max(widest, iframeWidth);
      }
    });

    const descendants = content.querySelectorAll("*");
    descendants.forEach(function (element) {
      widest = Math.max(widest, element.scrollWidth);
      widest = Math.max(widest, element.getBoundingClientRect().width);
    });

    return Math.ceil(widest);
  };

  const getIntrinsicContentMetrics = function (content) {
    const contentRect = content.getBoundingClientRect();
    let minLeft = 0;
    let maxRight = getIntrinsicContentWidth(content);
    let maxBottom = content.scrollHeight;

    const descendants = content.querySelectorAll("*");
    descendants.forEach(function (element) {
      const rect = element.getBoundingClientRect();
      if (!rect.width && !rect.height) {
        return;
      }

      const relativeLeft = rect.left - contentRect.left;
      const relativeRight = rect.right - contentRect.left;
      const relativeBottom = rect.bottom - contentRect.top;

      minLeft = Math.min(minLeft, relativeLeft);
      maxRight = Math.max(maxRight, relativeRight);
      maxBottom = Math.max(maxBottom, relativeBottom);
    });

    return {
      width: Math.ceil(maxRight - minLeft),
      height: Math.ceil(maxBottom),
    };
  };

  const clearMobileScale = function (scrollArea, content) {
    content.style.zoom = "";
    content.style.transform = "";
    content.style.transformOrigin = "";
    content.style.display = "";
    content.style.width = "";
    scrollArea.style.minHeight = "";
  };

  const applyMobileScale = function (scrollArea, content) {
    const isLandscapeMobile = landscapeMediaQuery.matches;
    if (!mobileMediaQuery.matches && !isLandscapeMobile) {
      clearMobileScale(scrollArea, content);
      return;
    }

    clearMobileScale(scrollArea, content);

    const contentMetrics = getIntrinsicContentMetrics(content);
    const contentWidth = contentMetrics.width;
    const contentHeight = contentMetrics.height;
    const viewportWidth = scrollArea.clientWidth;

    if (!contentWidth || !viewportWidth) {
      return;
    }

    const fitWidth = Math.max(1, viewportWidth - 8);
    // In landscape, use the full viewport height so the embed is correctly sized
    // regardless of where it sits on the page (avoids tiny-then-grows-on-scroll).
    const viewportTop = isLandscapeMobile ? 0 : Math.max(0, scrollArea.getBoundingClientRect().top);
    const fitHeight = Math.max(1, window.innerHeight - viewportTop - 12);
    const widthScale = fitWidth / contentWidth;
    const heightScale = fitHeight / Math.max(1, contentHeight);
    // In landscape: scale to fill the width; height overflow is handled by the scroll container.
    // In portrait: scale to fit both dimensions, capped at 1 to avoid upscaling.
    const scale = isLandscapeMobile
      ? widthScale
      : Math.min(1, widthScale, heightScale);

    content.style.display = "block";
    content.style.width = `${contentWidth}px`;
    content.style.transformOrigin = "top left";
    content.style.transform = `scale(${scale.toFixed(4)})`;

    if (contentHeight) {
      const scaledHeight = Math.ceil(contentHeight * scale);
      // In landscape, cap the container to the viewport height so the page doesn't grow
      // taller than the screen; the scroll area's overflow:auto handles the rest.
      scrollArea.style.minHeight = isLandscapeMobile
        ? `${Math.min(scaledHeight, Math.ceil(window.innerHeight - 12))}px`
        : `${scaledHeight}px`;
    }

    scrollArea.scrollLeft = 0;
  };

  embedBlocks.forEach(function (block) {
    const scrollArea = block.querySelector(".js-code-embed-scroll-hip");
    if (!scrollArea) {
      return;
    }

    const content = scrollArea.querySelector(".code-embed-content-hip");
    if (!content) {
      return;
    }

    const scaleToViewport = function () {
      applyMobileScale(scrollArea, content);
    };

    let hasPendingScale = false;

    const scheduleScaleToViewport = function () {
      if (hasPendingScale) {
        return;
      }

      hasPendingScale = true;
      window.requestAnimationFrame(function () {
        hasPendingScale = false;
        scaleToViewport();
      });
    };

    scheduleScaleToViewport();

    const hideHintOnInteraction = function () {
      if (!mobileMediaQuery.matches && !landscapeMediaQuery.matches) {
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
        scheduleScaleToViewport();
        iframe.style.touchAction = "auto";
      });
    }

    if (window.ResizeObserver) {
      const resizeObserver = new window.ResizeObserver(scheduleScaleToViewport);
      resizeObserver.observe(scrollArea);
      resizeObserver.observe(content);
    }

    if (window.MutationObserver) {
      const mutationObserver = new window.MutationObserver(scheduleScaleToViewport);
      mutationObserver.observe(content, {
        childList: true,
        subtree: true,
        attributes: true,
      });
    }

    mobileMediaQuery.addEventListener("change", scheduleScaleToViewport);
    landscapeMediaQuery.addEventListener("change", scheduleScaleToViewport);
    window.addEventListener("resize", scheduleScaleToViewport, { passive: true });
    window.addEventListener("orientationchange", scheduleScaleToViewport, { passive: true });
  });
}
