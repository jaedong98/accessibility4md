---
marp: true
theme: uncover
class: invert
---

# <!--fill--> Accessibililty Checker for Markdown :arrow_down:

##### Feb 14, 2023
##### Jae Dong Hwang


---

# Accessbility in markdown publication

```markdown
# My TODO List

Hello World
```
:arrow_down:

```html
<h1>My TODO List</h1>
<p>Hello World</p>
```

- High Adapatbility in code repository, i.e., README.md
- Used in many blog posts.
- Many preview or transformer tools don't validate the accessibility.

---
# Promise & Project Goal
* Find the accessibility issue in compile time and help people to publish the web contents with accessibility.
  * Educate and enforce the accessibility standards.
* Study and deliver a extensible tool that checks the accessibility of the markdown.

---
# Proposed Approach
- Implement the checker using [python-markdown extension API](https://python-markdown.github.io/extensions/api/).
- The parser loads text, applies the `preprocessors`, creates and builds an ElementTree object from the `block processors` and `inline processors`, renders the ElementTree object as Unicode text, and then then applies the `postprocessors`.
- Plan to extend the library to check the various accessibility of the contents in the markdown document.
---
# Project Plan(timeline)
- Week 1. Feasibility Study - Be familiar with langage and library.
- Week 2. Scope down the cases to demonstrate the feature.
- Week 3. Implementation.
- Week 4. Document the development process and publish as a website.

---
# Deliverables
* Executable Accessibility Checker for targeted cases.
* Project Website that includes
  * Design and Deliverables
  * Results
  * Challanges Encountered
  * Potential extensibility