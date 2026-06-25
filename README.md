# Minwoo Kang academic website preview

This is a static, GitHub Pages-ready website.

## Preview locally

GitHub Desktop users can open the repository in a terminal and run:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

The Publications page now also works when opened directly because its data are bundled in `data/publications.js`. Running a local server is still recommended for final testing.

## Publish with GitHub Pages

1. Create a public repository named `minwookang91-creator.github.io`.
2. Copy all files from this folder into the repository.
3. Commit and push in GitHub Desktop.
4. In the repository, open **Settings → Pages**.
5. Under **Build and deployment**, select **Deploy from a branch**.
6. Select branch `main` and folder `/ (root)`.
7. The site will appear at `https://minwookang91-creator.github.io`.

## Publications workflow

- The website reads `data/publications.json`.
- Entries can always be edited manually.
- `.github/workflows/update-publications.yml` checks Crossref weekly for works carrying ORCID `0000-0002-1982-9818`.
- Crossref ORCID coverage is incomplete, so automated additions must be reviewed.
- Manual fields such as `status`, `featured`, and `abstract` are preserved for existing entries.

## Research images

The current research graphics are original conceptual SVG/CSS illustrations. Replace them later with selected panels from your papers or preprints after checking image licensing and adding an appropriate citation.
