---
marp: true
theme: uncover
#class: invert
---

# <!--fill--> Accessibililty Checker for Markdown :arrow_down:

##### Feb 14, 2023
##### Jae Dong Hwang


---

# What is Markdown :question:

```markdown
# My TODO List

Hello World
```
:arrow_down:

```html
<h1>My TODO List</h1>
<p>Hello World</p>
```

---
# Project Goal
* Extend open source markdown compiler library to check the accessibility of markdown file.
* Provide the feedback to the publisher in a compile time.
* Share the challanges identified during development.

---
# Proposed Approach
- Implement the checker using [python-markdown extension API](https://python-markdown.github.io/extensions/api/).
- The parser loads text, applies the `preprocessors`, creates and builds an ElementTree object from the `block processors` and `inline processors`, renders the ElementTree object as Unicode text, and then then applies the `postprocessors`.

---
# Project Plan
- Feasibility Study - Be familiar with langage and library.
- Scope down the cases to demonstrate the feature.
  - Goal: 2 easy, 1 medium, and 1 hard
- Implementation.
- Document the development process and publish as a website.

---
# Deliverables
* Executable Accessibility Checker for targeted cases.
* Project Website that includes
  * Design and Deliverables
  * Results
  * Challanges Encountered
  * Potential extensibility