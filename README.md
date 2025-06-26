- 👋 Hi, I’m @Ahmed-aiu
- 👀 I’m interested in learning how to build custom AI models
- 🌱 I’m currently learning how to train deep neural nets
- 💞️ I’m looking to collaborate on AI projects
- 📫 How to reach me Email
- 😄 Pronouns: Ahh! med
- ⚡ Fun fact: I am in the middle of reinventing myself!

<!---
Ahmed-aiu/Ahmed-aiu is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Static Frontend

The repository contains a small static site under `static/`. The page
`static/html/rfq_distribution_static.html` can be used as the main entry
point for GitHub Pages. Either rename this file to `index.html` so it is
served automatically or link to it directly from `index.html`.

Commit the whole `static/` directory to the repository and then enable
GitHub Pages from the repository settings, selecting the default branch
as the source. After enabling Pages the HTML files in `static/` will be
served under your GitHub Pages URL.

## Backend JSON output

The backend responds with JSON summarising an RFQ. The format is shown
in the comments of `ai_rfq_analysis.py`:

```json
{"Summary": "SUMMARY",
 "Main-Categories": {"Main Category 1": "<top-category-1>",
                     "Main Category 2": "<top-category-2>"},
 "Sub-Categories": {"Sub Category 1": "<work activity 1>",
                    "Sub Category 2": "<work activity 2>",
                    "Sub Category 3": "<work activity 3>"},
 "Departments": {"Department-1": {"Name": "<department-1>",
                                   "Share": "responsibility-share-department-1",
                                   "Contact": "contact-person-1"},
                 "Department-2": {"Name": "<department-2>",
                                   "Share": "responsibility-share-department-2",
                                   "Contact": "contact-person-2"}},
 "Project-Start": "PSTART",
 "Project-Duration": "PDURATION",
 "Proposal-Deadline": "DEADLINE",
 "Contact-Technical": "CONTACTTECH",
 "Contact-Commercial": "CONTACTCOMM"}
```

Example response:

```json
{"Summary": "ABC Automotive GmbH is seeking a qualified engineering service provider to develop the software of an electric powertrain for a new model of electric SUV ...",
 "Main-Categories": {"Main Category 1": "VCU or Vehicle Control Unit or Powertrain Control Unit or Powertrain Domain Controller"},
 "Sub-Categories": {"Sub Category 1": "VCU Software",
                    "Sub Category 2": "VCU Hardware"},
 "Departments": {"Department-1": {"Name": "BES-C",
                                   "Share": "100 %"}}}
```
