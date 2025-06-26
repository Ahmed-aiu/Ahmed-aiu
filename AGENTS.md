This repository contains a small static site under `static/` and Python scripts in `a_rfq_distribution/py` used to analyse RFQs.

Key points
----------
- `static/html/rfq_distribution_static.html` can be used as the site entry page for GitHub Pages. Either rename it to `index.html` or link to it from an `index.html` file.
- Commit the entire `static/` directory when adding the site and enable GitHub Pages from the repository settings so that these files are hosted.
- The backend JSON structure expected by `ai_rfq_analysis.py` is documented in the comments of that file and summarised in the README. Refer to it when updating the API or documentation.

Workflow tips
-------------
- Run `git status --short` before and after your changes to ensure the work tree is clean.
- There are no automated tests. Manual verification is expected.
- Keep commit messages short but clear (one line summary).
- Always include relevant files in commits, especially static assets under `static/`.
- Review this AGENTS.md for repo guidelines whenever starting a new task.
