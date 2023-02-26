# Deliverables
## Project pitch slides. - Completed 2/14
## Functional Requirement Spec - Word document
  |WCAG Criteria| Requirement | Priority |
  |-|-|-|
  |1.1.1 Non-Content – Level A|  The tool iterates any links and checks whether the alternative text is provided.| P0 |
  |1.3.1 Info and Relationships and 1.3.2 Meaningful Sequence – Level A|The tool checks the structure in the markdown and whether there is a missing sequence.| P0 |
  |1.4.3 Contrast (Minimum) – Level AA|The tool checks whether the linked image of text has a contrast ratio of at least 4.5:1.|P1|
  |1.4.11 Non-text Contrast – Level AA|The tool checks the image in the file has ta contrast ratio of at least 3:1 against adjacent color(s).|P1|
  |2.4.2 Page Titled – Level A | The first heading should be a level one heading and should be the same or nearly the same as the file name. The first level on heading is used as the page `<title>`. Tool warns on missing title.| P0 |
  |2.4.4 Link Purpose (In Context) – Level A and 2.4.9 Link Purpose (Link Only)|The tool should check whether any link provided text has the description of the purpose of a link.| P0 |
  |2.4.10 Section Heading – Level AAA| This might be little tricky to determine the missing section heading in markdown file. |TBD|
  |3.1.4 Abbreviations – Level AAA |This might be the extended feature if time is allowed. Tool checks the abbreviation in the contents and provides feedback on whether it has the definition in place. |Extended Goal|

## Project ReadMe/Website
  - Project Purpose and Scope
  - Study results on the extensibility.
  - Challanges.
  - Potential Future work.
    - Extends the prototyped extension module to catch more accessibility issue.
    - Improved feedback loop (enhance logging or highlight the error in html.)
    - Integrate with existing markdown preview pluging - AccessibilityChecker Preview.

## Some extensible ideas
- The checker to support extended markdown syntax that allow auther to insert **[ARIA](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)** attributees, role and property. For example, we can add each `role="list"` in the list element to produce the html ([example](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/list_role)).
  ```html
  <div role="list">
    <div role="listitem">List item 1</div>
    <div role="listitem">List item 2</div>
    <div role="listitem">List item 3</div>
  </div>
  ```
