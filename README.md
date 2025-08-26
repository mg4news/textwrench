# Text Wrench

A set of tools to modify and manipulate text files, particularly markdown files. I created these because I use Obsidian for pretty much everything:
- authoring documents (md -> html -> pdf)
- research
- patent analysis
- project tracking (kanban)
- etc. 

This lets me berform file and batch (directory) operations that are not supported by Obsidian plugins, such as:
- converting the TOC plugin to a table of contents that is still selectable after conversion to PDF
- bulk changes accross categories of files

## About

### Audience
Anyone who writes and publishes documents, and is looking for a workflow the that:
- allows for easy creation of well formatted documents without the need for proprietary tools
- allows the documents to be published in a standard way (i.e. PDF or HTML)

### Workflow Requirements
Key requirements:
- Accessible: the authoring system must be easy to access, create, edit, and rev documents.  
- Usable by the widest range of authors: engineers, architects, product managers, and marketing leads
- Web-based with alternative interfaces as desired.
- No VPN connection required; make it easy to dip in-and-out from anywhere
- No authoring-environment-specific requirements: uses MD or something dead-simple. No Docker images, no python scripting.
- Programmatic Interface: required for maintenance and external editor access.
- Distributed Version Control: Best Practice, necessary.
- Integrated Publishing Environment: a single system would be used to publish and manage docs, if just for the sake of simplicity and accessibility.
- TOC: the docus need a table of contents, and it must be navigable (clickable) in the final PDF. 

## Install requirements
To generate PDF via HTML, you will need to install:
- pandoc (see https://pandoc.org/index.html)
- weasyprint (I used `brew install weasyprint`)

## Usage
My normal workflow is:
- author a complex dovument in Obsidian using the markdown "templates" from the `/data` directory
- the main document body is based on the main document schema
- chapters are separate linked markdown docs based on the chapters schema, and are referenced by links, i.e. `[[chapter_x.md]]`
- run TextWrench:, which:
  - optionally assembles a single markdown document from the linked documents
  - optionally replaces the TOC marker (YAML) with an HTML/PDF friendly TOC
  - saves the intermediate markdown
  - runs pandoc and weasyprint with a specified style sheet to generate a PDF 

## Notes

### Embedding Images 
If you use the normal markdown syntax for embedding images (e.g. ```![Logo](../../images/SomeCompanyLogo.png)```) you can use relative paths (e.g. ../../image). However, this syntax does not give control over alignment.
If you use HTML:

```<img align="right" src="../../images/SomeCompanyLogo.png">```

Then you can align the image, and the MD presents correctly on github. However, it does not present correctly in a local environment. You can use relative paths with HTML, but you cannot navigate back up the tree. 

