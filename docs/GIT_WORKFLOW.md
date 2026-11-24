# 🌿 Git workflow for beginners

You only need **6 commands**. Never work directly on `main` for figure work: use a branch, then a Pull Request (PR) that a teammate reviews. That review is how we all stay in control.

## Every time you start working
```bash
git checkout main
git pull                      # get everyone else's latest work
git checkout -b fig2-competition     # new branch (name = what you're doing)
```

## While working (often!)
```bash
git status                    # what changed?
git add scripts/fig2_competition.py figures/fig2_competition.png
git commit -m "fig2: stimulation trial works, old bump suppressed"
git push -u origin fig2-competition   # first time; afterwards just `git push`
```

## When a step is done
1. On GitHub you'll see **"Compare & pull request"**. Click it.
2. Title: `Fig 2: steps 1–2`. In the description: what you did, a screenshot of the figure, and `Closes #<issue number>`.
3. Assign the **reviewer** from PLAN.md.
4. Reviewer: pull the branch, **run it**, ask questions in comments, then **Approve** → **Merge**.
   ```bash
   git fetch && git checkout fig2-competition && python scripts/fig2_competition.py
   ```

## Small edits (ticking a box in PLAN.md, meeting notes)
Fine to commit directly to `main`: `git pull` → edit → `git commit -am "plan: tick tutorial"` → `git push`.

## Rules that prevent pain
- **Pull before you start, push when you stop.** Every session.
- Don't commit: the paper PDF, data files, `.venv/`, huge results. `.gitignore` already blocks most of these.
- Notebooks: **clear outputs before committing** (Kernel → Restart & Clear Output). Otherwise merges become messy.
- Two people editing the same file at the same time → merge conflict. Avoid it by owning different files (that's why every figure has its own script).
- Got a merge conflict? Don't panic. Open the file, look for `<<<<<<<` / `>>>>>>>`, keep the right lines, delete the markers, `git add` + `git commit`. Or ask in the group chat.

## Commit message style
`<area>: <what changed>`, e.g. `model: add WTA connectivity`, `fig3: histogram of drift distances`, `docs: meeting notes 2 Dec`.
