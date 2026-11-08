# Calm Minds study: codebook

A (fictional) study with 120 participants on whether a **mindfulness app** reduces anxiety compared to a **control app**.
Participants filled in the same questionnaire three times: before the study (**pre**), after 4 weeks (**post**) and after 12 weeks (**follow-up**).

| Column | What it should contain |
|---|---|
| `ID` | Participant code (P001 – P120) |
| `wave` | pre / post / follow-up |
| `Date` | Date of the questionnaire |
| `Age` | Age in years |
| `gender` | Gender (self-reported) |
| `Condition` | control or treatment |
| `anxiety_1`, `anxiety_2`, `Anx3`, `anx_4R`, `ANXIETY 5`, `anx.6` | Six anxiety items, 1 (not at all) to 5 (very much). Item 4 is phrased positively ("I feel calm"). |
| `attn_check` | Attention check: "Please select 4 for this question." |
| `sleep_hrs` | Average hours of sleep per night last week |
| `stroop_RT_ms` | Mean reaction time on a Stroop task, in milliseconds |

That's what the data *should* look like. Whether it actually does… is for you to find out. 🕵️
