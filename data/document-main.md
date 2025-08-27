<!--
title: "Main Document Template"
author: "Martin Gibson"
date: "2020-01-12"
-->

<!--
Template for a document "main" with
- A logo image, top right aligned
- Title, centre aligned
- Basic TOC structure
- Page breaks for the MD->HTML-PDF conversion

Note:
To right align an image you would need:
<img align="right" src="../images/some_logo_image.png">
This will display properly on GitHub but may not display locally,
nor will it convert to PDF properly (since we run the conversion locally)
So fallback to using markdown only for now...

YOU MUST:
- Adjust the relative path to the logo
- Change the <title> tag (just to satisfy the conversion).
- Change the front page (L1 header, version)
- Update the "Document Purpose" and ""Audience" content in the "Preface"
- The rest of the Sections (overview and onwards are up to you)
- Update the TOC and headers to match your needs
- Update the acronym table
- Update the version table

TO ADD CHAPTERS
- create the chapter as a separate file using the Doc Chapter Template. 
- link in the chapter note, i.e. : [[document_chapXX]]
- prefix the link with ! to see the contents in place

## Chapter X
<br/>
[[Chapter X]]
-->


![Logo](images/tux.png)

<br/>
<br/>

<p style="text-align: center; font-size: 32px; font-weight: bold;">
  Document title
</p>

<br/>
<br/>

<p style="text-align: center; font-size: 18px; font-weight: bold;">
  Version 0.0.1 (draft)
</p>

<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
<!---------------------------------------------------------------------------------------
See https://github.com/ActiveVideo/docs/blob/main/templates/basic.md for original CSS annotated 
TOC logic. Initially we are trying the Obsidian TOC plugin to see if that works with thte HTML, pandoc workflow. If it doesn't we will fallback to 
---------------------------------------------------------------------------------------->
```toc
min_depth: 1
max_depth: 3
```
<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
# Preface

## Copyright
No part of this document may be reproduced or transmitted in any form or by any means electronic or mechanical, for any purpose without the express written permission of Some Company. Information in this document is subject to change without prior notice. <br/>
Certain names of program products and company names used in this document might be registered trademarks or trademarks owned by other entities.
<br/>
<br/>
Some Company<br/>
123 Some St<br/>
Some City<br/>
Some State, and Zip<br/>

## Document Purpose
What the document covers 

## Audience
Who the document is intended for. 

## Conventions
### Language Conventions
This document uses specific language conventions to avoid ambiguity. Requirement levels are as defined in IETF RFC2119 (see https://www.ietf.org/rfc/rfc2119.txt). Specifically:
- The use of “shall”, “must” or “required” indicates a requirement
- The use of “must not” or “shall not” indicates a prohibition
- The use of “should” or “recommended” indicates a recommendation.
- The use of “may” indicates an option

### Additional conventions:
- *Text in italics is for information only, and is not normative*
- `Text in fixed width font pertains to code specifics (function names, types, etc.)`
- Dates are expressed in ANSI standard format, i.e., YYYY-MM-DD

### Document Change Policy
The document shall be maintained and updated by TOP LLC. All changes shall be versioned. All functional changes shall be reviewed and accepted by representatives of all of the working tracks. 

### Related Documents
- list of related documents, if any

### Document history
| Date       | Author        | Description |
| ---------- | ------------- | ----------- |
| 2025-07-24 | Martin Gibson | Draft       |

### Terms and Acronyms
| Term   | Description                            |
| ------ | -------------------------------------- |
| API    | Application Programming Interface      |
| TLA    | Three Leter Acronym                    |


<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
# Overview

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Some Detailed Topic

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
[[document-chap01]]

<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
[[document-chap02]]

<!---------------------------------------------------------------------------------------
Generate a page break in PDF output
---------------------------------------------------------------------------------------->
<div style="page-break-after: always;"></div>

---
[[document-appendix]]

