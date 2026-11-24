#!/usr/bin/env bash
# Creates labels, 3 milestones and one issue per task from PLAN.md on GitHub.
# Run ONCE, from the repo folder, after pushing it to GitHub:
#
#   gh auth login                       # once, if not logged in
#   JULIA=julia-gh LUIZ=luiz-gh ELIZABETH=eliz-gh bash tools/setup_github.sh
#
# (Replace with your real GitHub usernames so issues get assigned.
#  Leave them out and issues are created unassigned.)
set -euo pipefail

command -v gh >/dev/null || { echo "Install the GitHub CLI first: https://cli.github.com"; exit 1; }
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Setting up $REPO"

J=${JULIA:-}; L=${LUIZ:-}; E=${ELIZABETH:-}

# ---- labels -----------------------------------------------------------------
label () { gh label create "$1" --color "$2" --description "$3" --force >/dev/null; }
label "julia"      "e99695" "Owner: Julia"
label "luiz"       "84b6eb" "Owner: Luiz"
label "elizabeth"  "c2e0c6" "Owner: Elizabeth"
label "everyone"   "fbca04" "Each of us does this"
label "setup"      "bfdadc" "Phase 0"
label "understand" "d4c5f9" "Phase 1"
label "simulate"   "0e8a16" "Phase 2"
label "present"    "b60205" "Phase 3"

# ---- milestones -------------------------------------------------------------
ms () { gh api "repos/$REPO/milestones" -f title="$1" -f due_on="$2" -f description="$3" >/dev/null 2>&1 || true; }
ms "M1 Understand" "2026-11-29T22:00:00Z" "Everyone can explain the model and Figs 1-4"
ms "M2 Simulate"   "2026-12-06T22:00:00Z" "All model figures exist (draft quality)"
ms "M3 Present"    "2026-12-14T22:00:00Z" "Final slides, rehearsed at <= 20 min"

# ---- issues -----------------------------------------------------------------
# issue "<title>" "<labels>" "<milestone>" "<assignee or empty>" "<body>"
issue () {
  args=(--title "$1" --label "$2" --milestone "$3" --body "$5")
  [ -n "$4" ] && args+=(--assignee "$4")
  gh issue create "${args[@]}" >/dev/null && echo "  + $1"
}

echo "Creating issues..."
issue "Install env + run pytest (Julia)"     "setup,everyone,julia"     "M1 Understand" "$J" "pip install -r requirements.txt && pytest -q -> 13 passed"
issue "Install env + run pytest (Luiz)"      "setup,everyone,luiz"      "M1 Understand" "$L" "pip install -r requirements.txt && pytest -q -> 13 passed"
issue "Install env + run pytest (Elizabeth)" "setup,everyone,elizabeth" "M1 Understand" "$E" "pip install -r requirements.txt && pytest -q -> 13 passed"
issue "Get supplementary materials (fig. S3, S4, Supp. Text)" "setup,luiz" "M1 Understand" "$L" "Download from the Science website, keep in papers/ (not committed)."
issue "Tutorial 01 (Julia)"     "understand,everyone,julia"     "M1 Understand" "$J" "notebooks/01_tutorial_first_bump.ipynb incl. exercises. Reviewer: Elizabeth"
issue "Tutorial 01 (Luiz)"      "understand,everyone,luiz"      "M1 Understand" "$L" "notebooks/01_tutorial_first_bump.ipynb incl. exercises. Reviewer: Julia"
issue "Tutorial 01 (Elizabeth)" "understand,everyone,elizabeth" "M1 Understand" "$E" "notebooks/01_tutorial_first_bump.ipynb incl. exercises. Reviewer: Luiz"
issue "Read the paper (reading guide in docs/PAPER_NOTES.md)" "understand,everyone" "M1 Understand" "" "Pass 1 + pass 2 before Fri 27 Nov meeting."
issue "Biology cheat sheet in PAPER_NOTES.md"        "understand,julia"     "M1 Understand" "$J" "5-8 bullets. Reviewer: Elizabeth"
issue "Model in plain words in PAPER_NOTES.md"       "understand,luiz"      "M1 Understand" "$L" "Reviewer: Julia"
issue "Experiments in plain words in PAPER_NOTES.md" "understand,elizabeth" "M1 Understand" "$E" "Reviewer: Luiz"
issue "Meeting Fri 27 Nov: each explains one figure" "understand,everyone" "M1 Understand" "" "Julia: Fig 1, Elizabeth: Fig 2+3, Luiz: Fig 4"

issue "Fig 1: tracking & darkness"            "simulate,julia"     "M2 Simulate" "$J" "scripts/fig1_tracking_and_darkness.py - steps 1-6. Reviewer: Elizabeth"
issue "Fig 1 STRETCH: real data PVA"           "simulate,julia"     "M2 Simulate" "$J" "Optional. See data/README.md"
issue "Fig 2: competition between bumps"       "simulate,elizabeth" "M2 Simulate" "$E" "scripts/fig2_competition.py - steps 1-5. Reviewer: Luiz"
issue "Fig 3: drift after stimulation, local vs WTA" "simulate,elizabeth" "M2 Simulate" "$E" "scripts/fig3_drift.py - steps 1-5. Reviewer: Luiz"
issue "Fig 4D: run, understand, explain to Julia" "simulate,luiz"   "M2 Simulate" "$L" "scripts/fig4_jump_vs_flow.py. Reviewer: Julia"
issue "Fig 4G: jump threshold 90 vs 180 + parameter study" "simulate,luiz" "M2 Simulate" "$L" "scripts/fig4G_jump_threshold.py - steps 1-6. Reviewer: Julia"
issue "RESULTS_LOG.md: one paragraph per figure" "simulate,everyone" "M2 Simulate" "" "Each owner writes their section."
issue "Meeting Wed 2 Dec: first plots"          "simulate,everyone" "M2 Simulate" "" ""
issue "Meeting Sun 6 Dec: M2 review + story of the talk" "simulate,everyone" "M2 Simulate" "" "Finalise docs/PRESENTATION_OUTLINE.md"

issue "Slide deck template + shared link"          "present,julia"     "M3 Present" "$J" "Due Mon 7 Dec"
issue "Slides: intro, background, Fig 1"           "present,julia"     "M3 Present" "$J" "Due Wed 9 Dec. Reviewer: Elizabeth"
issue "Slides: model + Fig 4"                       "present,luiz"      "M3 Present" "$L" "Due Wed 9 Dec. Reviewer: Julia"
issue "Slides: Fig 2, Fig 3, limitations, conclusions" "present,elizabeth" "M3 Present" "$E" "Due Wed 9 Dec. Reviewer: Luiz"
issue "Figure polish: consistent style"             "present,luiz"      "M3 Present" "$L" "Same fonts/colours/labels. Due Wed 9 Dec"
issue "Rehearsal 1 (Thu 10 Dec)"                    "present,everyone"  "M3 Present" "" "Timed. Log in docs/PRESENTATION_OUTLINE.md"
issue "Likely questions + answers"                  "present,elizabeth" "M3 Present" "$E" "Due Sat 12 Dec"
issue "Rehearsal 2 (Mon 14 Dec)"                    "present,everyone"  "M3 Present" "" "Final, <= 20 min, with Q&A"
issue "Export PDF to presentation/ + tag v1.0"      "present,julia"     "M3 Present" "$J" "Mon 14 Dec"

echo "Done. Now create a Project board: repo -> Projects -> New project -> Board, and add these issues."
