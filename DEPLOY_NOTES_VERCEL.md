Vercel deployment notes

Issue:
- Vercel reported: "The pattern \"api/index.py\" defined in `functions` doesn't match any Serverless Functions inside the `api` directory." 
  This happens when the `functions` property in `vercel.json` references a key that Vercel can't match to actual files in the `api/` folder.

What I changed:
- Updated `vercel.json` to use a glob that matches Python functions in the `api/` directory and specified the Python runtime.

Changes made:
- vercel.json
  - Replaced the explicit key `"api/index.py"` under `functions` with `"api/*.py"`.
  - Added `"runtime": "python3.10"` for the functions entry.

Why this fixes it:
- The glob `api/*.py` matches any .py file inside the `api` folder (including `api/index.py`).
- Specifying the runtime ensures Vercel uses the correct Python runtime for your Flask WSGI app.

Extra checks done:
- Confirmed `api/index.py` defines a top-level Flask `app` WSGI object (required by Vercel).
- Confirmed `api/requirements.txt` lists Flask and Flask-SQLAlchemy.
- Ran a quick syntax/type check on `api/index.py` (no errors found).

How to redeploy (recommended):
1. Commit the changes:
```powershell
git add vercel.json DEPLOY_NOTES_VERSEL.md
git commit -m "vercel: make functions pattern match api/*.py and set python runtime"
```

2a. If deploying with Vercel CLI from this machine:
```powershell
# Install/ensure Vercel CLI is available
npm i -g vercel
# From the repo root
vercel deploy --prod
```

2b. If deploying via GitHub (push to the branch connected to Vercel):
```powershell
git push origin main
# Vercel will build/deploy automatically if the project is connected
```

Notes / next steps:
- If you need a specific Python minor version, change `python3.10` to the appropriate supported runtime (eg `python3.11`) depending on Vercel's supported runtimes at deploy time.
- If you prefer explicit per-file config, you can also use exact filenames as keys (for example `"api/index.py"`) but ensure paths and file types are correct and that Vercel recognizes them; the glob is more flexible.
- If you run into issues where Vercel still can't detect functions, ensure there are no leading BOMs or hidden extensions (like `index.py.txt`) and that files are committed to the repo.

If you'd like, I can also:
- Add a small GitHub Actions workflow to validate `vercel.json` before push.
- Switch runtime to a different Python version if required.
