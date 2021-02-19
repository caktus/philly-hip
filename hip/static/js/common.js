export default function () {
  manageDocumentLinks();

  function manageDocumentLinks () {
    /* Manage Document Links

    Currently document links are displayed slightly differently than
    other links on a page.

    This function finds links to documents. If found,
    the link color is changed to $dark-blue, and the associated icon
    is displayed if found as a sibling of the link's parent container.
    
    <td> <!-- some container tag -->
      <p><a href="/documents/path-to/document"</a></p>
      <span class="external-link-icon-hip pt-3 pl-4 is-hidden"></span>
    </td>
    */
    let links = document.getElementsByTagName("a");
    links = Array.from(links);
    const documentLinks = links.filter(link => link.href.includes("document"));
    documentLinks.forEach(link => {
      const documentIcon = link.parentElement.nextElementSibling;
      if (documentIcon) {
        link.classList.add("is-dark-blue");
        documentIcon.classList.remove("is-hidden");
      }
    });
  }
};