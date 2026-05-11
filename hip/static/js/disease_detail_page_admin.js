document.addEventListener('DOMContentLoaded', function () {
    // Warn before deleting a StreamField block that contains content.
    document.addEventListener('click', function (e) {
        var deleteBtn = e.target.closest('[id$="-delete"]');
        if (!deleteBtn) return;

        // Walk up to the stream-field block container
        var block = deleteBtn.closest('[data-contentpath]');
        if (!block) return;

        // Collect text from all contenteditable, textarea, and input elements
        var parts = [];
        block.querySelectorAll('[contenteditable="true"], textarea, input[type="text"]').forEach(function (el) {
            var text = (el.innerText || el.value || '').trim();
            if (text) parts.push(text);
        });

        if (parts.length === 0) return; // nothing to warn about

        // Build a short preview (first 120 chars)
        var preview = parts.join(' ').substring(0, 120);
        if (parts.join(' ').length > 120) preview += '…';

        // Find the block label
        var label = '';
        var header = block.querySelector('.w-panel__heading, .c-sf-block__header__title, h3');
        if (header) label = header.textContent.trim();

        var message = 'This' + (label ? ' "' + label + '"' : '') +
            ' section contains content:\n\n"' + preview + '"\n\nAre you sure you want to remove it?';

        if (!confirm(message)) {
            e.preventDefault();
            e.stopImmediatePropagation();
        }
    }, true); // capture phase so we fire before Wagtail's handler
});
