# Method review

Written before reading the independent reviews, so it isn't anchored on them.

## Claude's own review

1. **Role prompt.** "You are voting as a member of a legislature" asks for role-play. A model may imagine a partisan legislator rather than give its own judgment. "You must decide based on your own judgment" then conflicts with that.
2. **Sponsor line is first and salient.** Opening with the party makes it the most prominent cue, and may read as an instruction to treat it as relevant.
3. **Bipartisan signal.** A Republican backing a left-coded bill can be read as evidence the bill is moderate or has cross-party support. That's not the same as favoring a party. The current design can't tell these apart.
4. **Abstain is unexplained.** The `none` version allowed heavy abstaining, and a label may change whether a model is willing to act. Yes rate alone hides this.
5. **Tool order.** `reason` follows `vote` in the tool, so the reason can be a justification after the fact. The text version reasons first. This makes reasons hard to compare across formats. Toolie is parked, but the main run should still pick one primary format.
6. **Reasons aren't evidence of denial.** A model writing a short reason needn't list party. Absence from a one-sentence reason shows little, and I overstated it.
7. **Self-report is hypothetical and leading.** "Would your vote be affected...?" invites "no" as the socially correct answer. It also asks about a general disposition, not the vote it cast.
8. **Bill writing.** I wrote and labeled every bill myself, some are worded more favorably than others, and they aren't a representative sample. Most votes are near 0% or 100%, leaving little room to detect a flip.
9. **Selection.** The re-test picked the biggest gaps, so the 5 of 20 can't estimate a rate. The re-test also lacks the original's text-format audit.
10. **Default settings.** Temperature and provider defaults differ by model. Responses and raw tool calls weren't fully saved. `seed` doesn't control the model.
11. **Missing controls.** No placebo labels. Without them, "party" can't be separated from "any sponsor information".

## Points raised by Ryan in discussion

Added after the independent reviewers started, so they didn't see these.

1. **Real legislation can contaminate results.** Models may recall a real bill's sponsor and reception, and that memory can have a larger effect than the label. The main test uses newly written, reviewed bills. Real bills are at most a separate later comparison. A separate check records which party each model expects to propose each bill.
2. **Don't force a reason.** It can change the vote and is weak evidence of why a model chose. The main run asks for the vote only, in both formats.
3. **Strict output.** A response is valid only if it's exactly one allowed vote with nothing else, allowing case and surrounding whitespace. Everything else fails.
4. **Failures are counted, not hidden.** Invalid responses are kept, classified and reported per model and sponsor version. The primary analysis uses valid votes, with a check that treats invalid responses as non-yes.
5. **Toolie is parked.** Format effects get their own project later. The main run still needs one primary format.
6. **Validation and logging.** Save the prompt, raw response, model version, settings, finish reason and token use for every call. Retry only API errors, and log them. Test that versions differ only in sponsor text, and that each planned call has one saved result.
7. **More threads.** Use about 30, run models at the same time, and save as the run goes.

## Independent reviews and decisions

Three independent reviewers looked at the code and data: a survey methodologist, a statistician and a hostile peer reviewer. The methodologist read this file's first section first, so it wasn't blind to it, and the statistician noticed the file too.

### Corrections to pilot claims

| Earlier claim | Correction |
|---|---|
| "Votes flip" on 5 bills | 3 were yes/no flips. 2 were abstain-to-yes shifts. |
| "20 largest gaps" | Top 5 per model and format, covering 17 bills. One had a first-run gap of 0, and some picks depended on tie order. |
| "Neither model leans" | Only about the average sponsor gap, with CIs of about ±4 to 7 points. Effects can cancel, and it says nothing about policy lean. |
| "Models deny influence" | Not supported. The hypothetical question got a nearly constant "no", which may be true for most bills. One-sentence reasons aren't motives. |
| "Claude says yes more when a Republican backs a left bill" | Not supported generally. The better lead is abstention: Claude tool abstained 24 times under same-party sponsors and 0 times under cross-party sponsors, across 228 votes each. Post hoc. |

### Accepted changes

| Issue | Change | Source |
|---|---|---|
| Yes rate hides effects | Report yes, no and abstain. Primary lean metric uses yes minus no. | All three |
| Role-play makes using party legitimate | Remove the legislator role | All, Claude |
| Abstain undefined, "must decide" conflicts | Define all options, say each is acceptable | Methodologist |
| Sponsor first and salient | Move the sponsor after the bill, as a plain record line | All, Claude |
| No placebo | Add a "first-term member" arm | All, Claude |
| Reason can change the vote | Vote only | Ryan, reviewers |
| Option order can matter | Each of 6 orders once per bill and arm; remove "in this order" | Statistician |
| Failed calls could look like a party gap | Shuffle jobs globally. Re-queue API errors. Keep invalid responses as their own outcome. | Statistician |
| Float ties made p-values too low | Use exact integer arithmetic | Statistician (verified bug) |
| Unpinned settings | Pin models, set temperature to 1, save settings and raw responses | Methodologist, statistician |
| Loaded words in bills | Reword the most loaded bills | Methodologist |
| Claims without a plan | `PREREG.md` is frozen before collecting data | Statistician |
| Flat 10-repeat run is weak | Two-stage screen then confirm | Statistician |

### Disagreements and decisions

- **Scale first or controls first?** The peer reviewer wanted controls before scaling, and the statistician a 100-bill screen. Decision: run the screen at 100 bills with a placebo arm built in, since Ryan asked for 100, and it answers both.
- **Long bill summaries.** The methodologist wants a 100–200 word version, because one-sentence bills can make party act as information about the content. Decision: test long versions on confirmed bills in Stage 2, not all 100 now, because of cost and because I'd write every summary myself.
- **Formats.** Toolie is parked, so this run uses one format: forced tool call, vote only.
- **Self-report.** Removed from Stage 1, because the old version can't be compared with votes. A prediction test comes back in Stage 2, once there are confirmed effects to test it against.
- **Real bills.** The methodologist suggested adding them. Rejected for now, following Ryan's contamination point.

### Known limits that remain

- Claude wrote and coded the bills, and Claude is also a subject. The left/right labels are debatable. Results apply to these bills only.
- A placebo-versus-none gap only shows whether a neutral sponsor detail moves votes. It doesn't rule out every non-party explanation.
- Bipartisan-signal, feasibility and content explanations are untested until Stage 2 controls.
- Six repeats won't confirm single-bill flips. Stage 1 only picks bills for Stage 2.
- Results are for bare API calls with no system prompt, not any product.
