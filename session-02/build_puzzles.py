#!/usr/bin/env python3
"""Generates session-02.qmd (Practical 1 · R Puzzle Lab) from the puzzle list below.
Edit the PUZZLES list, then run:  python3 build_puzzles.py && quarto render session-02.qmd
"""
import html, json

def esc(s):
    return html.escape(s, quote=False)

# kind: "num" (value, tol) · "text" (accepted answers) · "set" (all tokens, any order) · "done" (self-check)
PUZZLES = [
  # ── Level 1 ───────────────────────────────────────────────────────────
  dict(level=1, title="How big is it?",
       task="How many <b>rows</b> does the dataset have?",
       kind="num", answer=351, tol=0,
       hint="There is a function that returns rows <em>and</em> columns at once. Or try <code>nrow()</code>.",
       solution="dim(d)     # 351 rows, 15 columns\nnrow(d)    # 351",
       note="Each row is one measurement, not one person. Keep that in mind!"),
  dict(level=1, title="Name tags",
       task="One column name contains a <b>space</b>. Which one?",
       kind="text", answer=["ANXIETY 5"],
       hint="<code>names(d)</code> lists all column names.",
       solution="names(d)\n\n# a name with a space needs backticks:\nd$`ANXIETY 5`",
       note="Spaces in names are legal but annoying: you need <code>`backticks`</code> to use them. That’s why we loaded with <code>check.names = FALSE</code>."),
  dict(level=1, title="First look",
       task="What is the <b>Age</b> in the <b>4th row</b>?",
       kind="num", answer=31, tol=0,
       hint="<code>d$Age</code> gives the whole column. Square brackets pick one element.",
       solution="head(d$Age)   # first 6 values\nd$Age[4]      # 31"),
  dict(level=1, title="Average age",
       task="What is the <b>mean Age</b>? (2 decimals)",
       kind="num", answer=49.75, tol=0.01,
       hint="<code>mean()</code>",
       solution="mean(d$Age)   # 49.75",
       note="Psychology students with an average age of almost 50? 🤔 Remember this number."),
  dict(level=1, title="The oldest participant",
       task="What is the <b>highest Age</b> in the data?",
       kind="num", answer=999, tol=0,
       hint="<code>max()</code>, or look at <code>sort(unique(d$Age))</code>.",
       solution="max(d$Age)              # 999\nsort(unique(d$Age))     # all different ages, sorted",
       note="Nobody is 999 years old. Somebody used 999 as a code for “unknown”. Detective work starts now."),
  # ── Level 2 ───────────────────────────────────────────────────────────
  dict(level=2, title="Suspicious ages",
       task="How many <b>rows</b> have an Age above 100?",
       kind="num", answer=11, tol=0,
       hint="<code>d$Age &gt; 100</code> gives TRUE/FALSE for every row. What happens if you <code>sum()</code> TRUEs?",
       solution="d$Age > 100              # TRUE / FALSE per row\nsum(d$Age > 100)         # 11\nd[d$Age > 100, ]          # show those rows"),
  dict(level=2, title="Who are they?",
       task="Which <b>participant IDs</b> have Age 999? (separate them with commas)",
       kind="set", answer=["P003", "P071", "P087"],
       hint="Combine a condition with <code>d$ID[ ... ]</code>. One person appears several times: <code>unique()</code> helps.",
       solution="unique(d$ID[d$Age == 999])   # \"P003\" \"P071\" \"P087\""),
  dict(level=2, title="Fix and recompute",
       task="Replace every 999 in Age by <code>NA</code>. What is the mean Age now? (2 decimals)",
       kind="num", answer=24.77, tol=0.01,
       hint="Assign into a selection: <code>d$Age[ condition ] &lt;- NA</code>. Then <code>mean()</code> needs one extra argument to skip NAs.",
       solution="d$Age[d$Age == 999] <- NA\nmean(d$Age, na.rm = TRUE)   # 24.77",
       note="Much better! (Are there other odd ages left? Look at <code>sort(unique(d$Age))</code> again…)"),
  dict(level=2, title="Holes everywhere",
       task="Count the <code>NA</code>s in every column. What is the <b>highest</b> number of missing values in one column?",
       kind="num", answer=122, tol=0,
       hint="<code>is.na(d)</code> is TRUE wherever a value is missing. <code>colSums()</code> adds up each column.",
       solution="colSums(is.na(d))   # anx.6 has 122\n# (if you already did puzzle 8, Age has 9 too)"),
  dict(level=2, title="How many genders?",
       task="Clean up <b>gender</b>: make everything lowercase and remove extra spaces. How many <b>different values</b> are left?",
       kind="num", answer=6, tol=0,
       hint="<code>table(d$gender)</code> shows all spellings. <code>tolower()</code> helps… but you might still get one too many. Look very carefully at the text.",
       solution="table(d$gender)                     # 9 different spellings\nlength(unique(tolower(d$gender)))    # 7?!  \"f \" has a trailing space\nclean <- trimws(tolower(d$gender))\nlength(unique(clean))                # 6"),
  # ── Level 3 ───────────────────────────────────────────────────────────
  dict(level=3, title="Find the anxiety items",
       task="The anxiety questions have messy names. How many columns <b>contain “anx”</b> in their name (any capitalisation)?",
       kind="num", answer=6, tol=0,
       hint="<code>grep(pattern, x, ignore.case = TRUE, value = TRUE)</code>",
       solution="anx <- grep(\"anx\", names(d), ignore.case = TRUE, value = TRUE)\nanx          # 6 names\nd[anx]       # just those columns",
       note="Picking columns by name is exactly what the Variables box in JASP does for you."),
  dict(level=3, title="Item averages",
       task="Compute the mean of every anxiety item (skip NAs). Which item has the <b>highest</b> mean?",
       kind="text", answer=["anx.6"],
       hint="<code>sapply(data, function)</code> runs a function on every column. Extra arguments go after the function.",
       solution="sapply(d[anx], mean, na.rm = TRUE)\n# anx.6 is highest (3.22)",
       note="The items are on a 1–5 scale. Are all these means plausible? Is anx.6 really different, or are the others pulled down by something?"),
  dict(level=3, title="Change over time",
       task="Mean <code>anxiety_1</code> per <b>wave</b> (pre / post / follow-up). In which wave is it <b>lowest</b>?",
       kind="text", answer=["follow-up", "followup", "follow up"],
       hint="<code>tapply(values, groups, function, ...)</code>, or <code>aggregate()</code>.",
       solution="tapply(d$anxiety_1, d$wave, mean, na.rm = TRUE)\n# follow-up 1.99 · post 2.29 · pre 2.52",
       note="Splitting by a group is what “Split by” does in JASP’s Descriptives."),
  dict(level=3, title="Commas and dots",
       task="<code>sleep_hrs</code> is stored as text, and some values use a comma (<code>7,5</code>). Turn it into numbers. What is the <b>mean sleep</b>? (2 decimals)",
       kind="num", answer=7.01, tol=0.01,
       hint="<code>gsub(\",\", \".\", x)</code> replaces commas, <code>as.numeric()</code> converts text to numbers.",
       solution="sleep <- as.numeric(gsub(\",\", \".\", d$sleep_hrs))\nmean(sleep, na.rm = TRUE)   # 7.01"),
  dict(level=3, title="Your first results table",
       task="Build a data frame with one row per anxiety item and the columns <code>variable</code>, <code>mean</code> and <code>sd</code> (rounded to 2 decimals). Anything strange in the SDs?",
       kind="done",
       hint="<code>data.frame(variable = anx, mean = ..., sd = ...)</code>. Reuse your <code>sapply()</code> from puzzle 12.",
       solution="data.frame(\n  variable = anx,\n  mean     = round(sapply(d[anx], mean, na.rm = TRUE), 2),\n  sd       = round(sapply(d[anx], sd,   na.rm = TRUE), 2),\n  row.names = NULL\n)\n#    variable mean   sd\n# 1 anxiety_1 2.28 9.62   <- an SD of 9.6 on a 1–5 scale?!\n# ...\n# 6     anx.6 3.22 0.86",
       note="An SD of almost 10 on a 1–5 scale… Try <code>table(d$anxiety_1)</code>. Another secret code! 🕵️"),
  # ── Level 4 ───────────────────────────────────────────────────────────
  dict(level=4, title="Your first function",
       task="Write <code>pct_missing(x)</code>: it returns the <b>percentage</b> of missing values in a vector. What does <code>pct_missing(d$anx.6)</code> give? (2 decimals)",
       kind="num", answer=34.76, tol=0.01,
       hint="<code>my_fun &lt;- function(x) { ... }</code>. The mean of TRUE/FALSE is the proportion of TRUEs.",
       solution="pct_missing <- function(x) {\n  100 * mean(is.na(x))\n}\npct_missing(d$anx.6)   # 34.76"),
  dict(level=4, title="A table-making function",
       task="Write <code>missing_table(df, vars)</code>: for the chosen columns, return a data frame with <code>variable</code>, <code>n_missing</code> and <code>pct_missing</code>. Run it on the anxiety items: what is the <b>sum</b> of <code>n_missing</code>?",
       kind="num", answer=134, tol=0,
       hint="Inside the function, <code>df[vars]</code> keeps only the chosen columns. You already know <code>colSums(is.na(...))</code>.",
       solution="missing_table <- function(df, vars) {\n  x <- df[vars]\n  n <- colSums(is.na(x))\n  data.frame(variable    = vars,\n             n_missing   = n,\n             pct_missing = round(100 * n / nrow(x), 1),\n             row.names   = NULL)\n}\nres <- missing_table(d, anx)\nsum(res$n_missing)   # 134",
       note="Data in, chosen variables in, a table out. That’s the shape of most JASP analyses…"),
  dict(level=4, title="Settings with defaults",
       task="Add two arguments: <code>codes = c(999, -99)</code> (values that also count as missing) and <code>digits = 1</code>. Run it again on the anxiety items: what is the new <b>sum</b> of <code>n_missing</code>?",
       kind="num", answer=144, tol=0,
       hint="Before counting, turn the codes into NA: <code>v[v %in% codes] &lt;- NA</code>. <code>lapply()</code> does that for every column.",
       solution="missing_table <- function(df, vars, codes = c(999, -99), digits = 1) {\n  x <- df[vars]\n  x[] <- lapply(x, function(v) { v[v %in% codes] <- NA; v })\n  n <- colSums(is.na(x))\n  data.frame(variable    = vars,\n             n_missing   = n,\n             pct_missing = round(100 * n / nrow(x), digits),\n             row.names   = NULL)\n}\nsum(missing_table(d, anx)$n_missing)   # 144",
       note="Arguments with defaults are like settings in an analysis window: they work out of the box, and users can change them."),
  dict(level=4, title="Make it user-proof",
       task="What happens if someone types a column that doesn’t exist, like <code>missing_table(d, \"Agee\")</code>? Make your function stop with a <b>friendly message</b> instead.",
       kind="done",
       hint="<code>setdiff(vars, names(df))</code> lists names that don’t exist. <code>stop(\"your message\")</code> ends the function with an error.",
       solution="missing_table <- function(df, vars, codes = c(999, -99), digits = 1) {\n  unknown <- setdiff(vars, names(df))\n  if (length(unknown) > 0)\n    stop(\"These columns don't exist: \", paste(unknown, collapse = \", \"))\n  # ... rest as before\n}\nmissing_table(d, \"Agee\")\n# Error: These columns don't exist: Agee",
       note="Good software expects users to make mistakes, and tells them what went wrong."),
  dict(level=4, title="Boss: mini-Descriptives 👑",
       task="Write <code>describe(df, vars, split_by = NULL)</code> that returns <code>n</code>, <code>mean</code> and <code>sd</code> for each variable, optionally <b>per group</b>. Run <code>describe(d, \"stroop_RT_ms\", split_by = \"wave\")</code>: which wave has the <b>highest mean</b> reaction time?",
       kind="text", answer=["follow-up", "followup", "follow up"],
       hint="Start without groups. Then: if <code>split_by</code> is not NULL, <code>split(df, df[[split_by]])</code> gives one data frame per group, and you can run your function on each of them.",
       solution="describe <- function(df, vars, split_by = NULL) {\n  one <- function(x) data.frame(\n    variable = vars,\n    n    = sapply(x[vars], function(v) sum(!is.na(v))),\n    mean = round(sapply(x[vars], mean, na.rm = TRUE), 1),\n    sd   = round(sapply(x[vars], sd,   na.rm = TRUE), 1),\n    row.names = NULL)\n  if (is.null(split_by)) return(one(df))\n  parts <- split(df, df[[split_by]])\n  out <- do.call(rbind, lapply(names(parts), function(g) cbind(group = g, one(parts[[g]]))))\n  out\n}\ndescribe(d, \"stroop_RT_ms\", split_by = \"wave\")\n#       group     variable   n  mean     sd\n# 1 follow-up stroop_RT_ms 108 869.1 2083.1\n# 2      post stroop_RT_ms 122 647.8  104.8\n# 3       pre stroop_RT_ms 121 839.0 1567.2",
       note="Look at those SDs: 2083 ms?! Something lives in the tails… but that’s a case for another day. 🕵️ You just wrote your own Descriptives. Next step: putting functions like this inside JASP."),
]


# 📘 Concept cards: shown just before the puzzle where the idea first appears
CONCEPTS = {
  1: ("Objects and functions",
      "<code>&lt;-</code> stores something under a name, so you can use it later. A <b>function</b> does something with the input you put between its brackets.",
      "x <- 5        # store 5 under the name x\nx * 2         # 10\n\ndim(d)        # a function: give it d, get back rows and columns"),
  3: ("Picking things: $ and [ ]",
      "<code>$</code> takes one column out of a data frame. Square brackets pick elements: <code>[i]</code> in a column, <code>[row, column]</code> in a data frame. Leave a side empty to get everything.",
      "d$Age          # the whole Age column\nd$Age[4]       # its 4th value\nd[4, ]         # the whole 4th row\nd[4, \"Age\"]    # row 4, column Age"),
  6: ("TRUE and FALSE",
      "A comparison checks every value and answers TRUE or FALSE. R counts TRUE as 1, so <code>sum()</code> counts them. Put TRUE/FALSE inside <code>[ ]</code> to keep only the TRUE rows.",
      "d$Age > 100            # TRUE / FALSE for every row\nsum(d$Age > 100)       # how many TRUEs\nd[d$Age > 100, ]       # only those rows\n# also: ==  !=  <  >=  & (and)  | (or)"),
  8: ("Missing values: NA",
      "<code>NA</code> means “unknown”. Any calculation with an unknown gives an unknown, unless you tell the function to skip it.",
      "mean(c(4, NA, 6))                # NA\nmean(c(4, NA, 6), na.rm = TRUE)  # 5\nis.na(c(4, NA, 6))               # FALSE TRUE FALSE\nx[x == 999] <- NA                # turn a code into NA"),
  10: ("Working with text",
      "Text needs to be exactly the same to count as the same: <code>\"Male\"</code>, <code>\"male\"</code> and <code>\"male \"</code> are three different values for R.",
      "tolower(\"Male\")          # \"male\"\ntrimws(\"  male \")        # \"male\"\ngsub(\",\", \".\", \"7,5\")    # \"7.5\"\ngrepl(\"anx\", \"Anx3\", ignore.case = TRUE)  # TRUE"),
  12: ("One function, many columns",
      "<code>sapply()</code> runs a function on every column and collects the results. Extra arguments for that function go at the end.",
      "sapply(d[c(\"Age\", \"anx.6\")], mean, na.rm = TRUE)\n#   Age  anx.6\n# 49.75   3.22"),
  15: ("Build your own data frame",
      "A data frame is a set of equally long columns. <code>c()</code> combines values into a column, <code>data.frame()</code> glues columns into a table.",
      "data.frame(\n  name  = c(\"a\", \"b\"),\n  score = c(10, 20)\n)\n#   name score\n# 1    a    10\n# 2    b    20"),
  16: ("Write your own function",
      "<code>function(arguments) { ... }</code> creates a function. The last line inside is what it gives back. Arguments can have defaults.",
      "double_it <- function(x, times = 2) {\n  x * times\n}\ndouble_it(5)             # 10\ndouble_it(5, times = 3)  # 15"),
}

CHEATSHEET = [
  ("Load", "d <- read.csv(file.choose(), check.names = FALSE)"),
  ("Look", "head(d) · str(d) · names(d) · dim(d) · nrow(d)"),
  ("Pick", "d$Age · d$Age[4] · d[4, ] · d[ , c(\"Age\", \"gender\")] · d$`ANXIETY 5`"),
  ("Compare", "==  !=  >  <  >=  <=  &  |  %in%"),
  ("Count", "sum(cond) · table(x) · unique(x) · length(x)"),
  ("Missing", "NA · is.na(x) · mean(x, na.rm = TRUE) · colSums(is.na(d))"),
  ("Change", "x[x == 999] <- NA · as.numeric(x)"),
  ("Text", "tolower(x) · trimws(x) · gsub(\",\", \".\", x) · grep(\"anx\", names(d), ignore.case = TRUE)"),
  ("Summarise", "mean · sd · max · min · round(x, 2)"),
  ("Many at once", "sapply(d[cols], mean, na.rm = TRUE) · tapply(x, group, mean)"),
  ("Build", "c(1, 2, 3) · data.frame(a = ..., b = ...) · split(d, d$wave)"),
  ("Function", "f <- function(x, y = 1) { ... }  ·  stop(\"message\")"),
  ("Help!", "?mean   (opens the help page of any function)"),
]

def concept_html(num):
    if num not in CONCEPTS: return ""
    t, txt, code = CONCEPTS[num]
    return (f'<div class="concept"><div class="concept-head"><span>📘</span><b>New idea</b><strong>{t}</strong></div>'
            f'<p>{txt}</p><pre><code>{esc(code)}</code></pre></div>')

def cheatsheet_html():
    rows = "".join(f'<tr><th>{k}</th><td><code>{esc(v)}</code></td></tr>' for k, v in CHEATSHEET)
    return ('<button type="button" class="cs-toggle" id="cs-toggle" aria-expanded="false" aria-controls="cs-panel">📘 R cheat sheet</button>'
            '<aside class="cs-panel" id="cs-panel" aria-label="R cheat sheet" hidden><div class="cs-head"><strong>📘 R cheat sheet</strong>'
            '<button type="button" class="cs-close" id="cs-close" aria-label="Close">✕</button></div>'
            f'<table data-quarto-disable-processing="true">{rows}</table></aside>')

LEVELS = {
  1: ("🌱", "Level 1 · First steps", "l1", "Never written R before? Start here."),
  2: ("🔍", "Level 2 · Detective", "l2", "Select, count and fix: the data has secrets."),
  3: ("🛠️", "Level 3 · Toolbox", "l3", "Everyday data-wrangling moves."),
  4: ("🚀", "Level 4 · Almost JASP", "l4", "Write your own functions that make tables."),
}

def puzzle_html(i, p):
    num = i + 1
    parts = [f'<div class="puz" id="puz-{num}" data-id="{num}" data-kind="{p["kind"]}">']
    parts.append(f'<div class="puz-head"><span class="puz-num">{num}</span><strong>{p["title"]}</strong><span class="puz-state" aria-live="polite"></span></div>')
    parts.append(f'<p class="puz-task">{p["task"]}</p>')
    if p["kind"] in ("num", "text", "set"):
        spec = {"kind": p["kind"]}
        if p["kind"] == "num":
            spec.update(answer=p["answer"], tol=p.get("tol", 0))
        else:
            spec.update(answer=p["answer"])
        parts.append('<div class="puz-check"><input type="text" class="puz-input" placeholder="Your answer" aria-label="Your answer">'
                     '<button type="button" class="puz-btn">Check</button>'
                     f'<script type="application/json" class="puz-spec">{json.dumps(spec)}</script></div>')
    else:
        parts.append('<div class="puz-check"><button type="button" class="puz-btn puz-done-btn">✓ I did it</button></div>')
    parts.append('<p class="puz-feedback" hidden></p>')
    if p.get("note"):
        parts.append(f'<p class="puz-note" hidden>{p["note"]}</p>')
    parts.append(f'<details class="stuck puz-hint"><summary>💡 Hint</summary><p>{p["hint"]}</p></details>')
    parts.append(f'<details class="stuck puz-sol"><summary>🔓 Solution</summary><pre><code>{esc(p["solution"])}</code></pre></details>')
    parts.append('</div>')
    return "".join(parts)

out = []
out.append('''---
title: "Practical 1: R Puzzle Lab"
format:
  html:
    title-block-style: none
    toc: false
    code-copy: true
    embed-resources: true
    theme: cosmo
    css: style.css
    include-in-header: head.html
    include-before-body: ribbon.html
    include-after-body: extras.html
    grid:
      body-width: 900px
---

<!-- GENERATED by build_puzzles.py: edit the script, not this file. -->

## Before you start {#start}

Twenty puzzles, one dataset, no JASP today: just you, R and a very messy study. **Pick any level you like**, skip what you already know, and help your neighbour. Solved a puzzle? Your progress is saved in this browser.

::::: {.steps}
:::: {.step}
[🌐 Browser]{.app .app-web} [Grab the data]{.step-title}

```{=html}
<div class="data-download"><a href="../data/calm_minds_mystery.csv" download>⬇️ Download calm_minds_mystery.csv</a> <a href="../data/codebook.html" target="_blank">📖 Codebook</a></div>
```
::::

:::: {.step}
[📊 RStudio]{.app .app-r} [Open a fresh script]{.step-title}

**File → New File → R Script.** Type your answers there, so you can save them.
::::

:::: {.step .step-final}
[📊 RStudio]{.app .app-r} [Load the data]{.step-title}

``` r
d <- read.csv(file.choose(), check.names = FALSE)
```

A window opens: pick the file you just downloaded. Now `d` is your dataset.
::::
:::::

```{=html}
<div class="puz-board" id="puz-board"></div>
''' + cheatsheet_html() + '''
```
''')
for lv in (1, 2, 3, 4):
    icon, name, anchor, blurb = LEVELS[lv]
    out.append(f"\n## {icon} {name} {{#{anchor}}}\n\n{blurb}\n\n```{{=html}}\n<div class=\"puz-level\" data-level=\"{lv}\">")
    for i, p in enumerate(PUZZLES):
        if p["level"] == lv:
            out.append(concept_html(i + 1) + puzzle_html(i, p))
    out.append("</div>\n```\n")

out.append('''
## Wrap-up {#wrapup}

```{=html}
<div class="next-cards">
  <div class="next-card session"><span class="next-when">Thu 26 Nov · 11:30–13:00 · 📍 REC JKK.26</span><strong>💡 Session 2</strong><p>Remember the functions you just wrote? Next time, one of them moves into JASP. 👀</p></div>
  <div class="next-card practical"><span class="next-when">Anytime</span><strong>🧩 Not finished?</strong><p>No rush: this page stays online. Questions? Post them on Mattermost.</p></div>
</div>
<div class="sign-off"><span class="sign-wave">👋</span><strong>Great detective work today!</strong><p>Until next time, and happy coding.</p><em>Leo &amp; the JASP Student Developers</em></div>
```
''')
open("session-02.qmd", "w").write("\n".join(out))
print("wrote session-02.qmd with", len(PUZZLES), "puzzles")
