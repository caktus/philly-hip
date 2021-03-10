export default function () {
  manageDocumentLinks();
  addExternalLinkIconsAndDomain();

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
        link.classList.add("is-dark-blue-hip");
        documentIcon.classList.remove("is-hidden");
      }
    });
  }

  function addExternalLinkIconsAndDomain () {
    /* Add External Link Icons to Wagtail Hook Generated Links of
    type external across the site.
     * Also, some external links get the link's domain inside of parentheses
     * added just after the icon. For example: for a link with an href to
     * cdc.gov/somethinig, we might add (cdc.gov) just after the icon.
     * We determine if the domain name needs to be added by seeing if the external
     * link is a child of an HTML element with a specific CSS class.
    */
   const externalLinks = Array.from(document.querySelectorAll('a.external-linktype'));

   // External links that are children of an HTML element with the following CSS
   // class will also get a domain name just after the icon.
   const parentsThatGetDomainForExternalLink = Array.from(document.querySelectorAll('.external-links-with-domains-hip'));

   for (const link of externalLinks) {
     // Add the external link icon.
     const span = document.createElement("span");
     span.classList.add("external-link-icon-hip");
     span.classList.add("pl-2");
     link.appendChild(span);

     // Is this link contained within one of the parentsThatGetDomainForExternalLink?
     let needToAddDomain = false;
     for (const parent of parentsThatGetDomainForExternalLink) {
       if (parent.contains(link) === true) {
         needToAddDomain = true;
         break;
       }
     }
     // If the link is a child of one of the parentsThatGetDomainForExternalLinks,
     // then add the domain name just after the external link icon.
     if (needToAddDomain === true) {
       const domainName = link.href.split("://").pop().split("/")[0];

       const domainSpan = document.createElement("span");
       domainSpan.innerHTML = `(${domainName})`;
       domainSpan.classList.add("external-link-domain-hip");
       domainSpan.classList.add("pl-2");
       link.appendChild(domainSpan);
     }
   };
  };
};
