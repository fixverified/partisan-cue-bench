# Methodology

This explains how partisan-cue-bench tries to reduce bias, why each choice was made, and what could still be wrong. It covers the current design. The analysis rules are in [`PREREG.md`](PREREG.md), and the reviews behind these changes are in [`METHOD_REVIEW.md`](METHOD_REVIEW.md).

## What the design can and can't show

The bill text is the same across versions, so a consistent vote difference can be attributed to the sponsor text.

That shows the label **moved the vote**. It doesn't show **why**. A model might favor a party, or it might treat the label as information about the bill's contents, its chances of passing, or whether it has bipartisan support.

## Bias controls

### Prompt

| Measure | Risk it reduces | Why |
|---|---|---|
| No legislator role | Accurate role-play being mistaken for bias | Real legislators use party cues, so asking a model to act as one makes using party legitimate |
| Sponsor listed after the bill as a plain record line | The label reading as the main thing to consider | The earlier version opened with the sponsor, the prompt's only fact apart from the bill |
| No required reason | Writing a reason changing the vote | A reason can also be written to justify a choice, so it's weak evidence of why a model chose |
| No system prompt, logged as such | Hidden instructions shaping answers | Consumer-product settings are a separate question |
| Fresh conversation per vote | Earlier answers influencing later ones | Models can't see or try to stay consistent with another version |
| Option text defined | Models interpreting yes and no differently | Each option is tied to supporting or opposing passage |
| No "in this order" wording | Drawing attention to the option sequence | The sequence itself is balanced below |
| Tests that versions differ only by sponsor | Accidental prompt differences | Runs on every test pass |

### Bills

| Measure | Risk it reduces | Why |
|---|---|---|
| Newly written bills | Models recalling a real bill's sponsor and reception | Memory could outweigh or mask the label |
| No names, party words or slogans in bill text | Extra political cues | The label should be the only party signal |
| Plainer wording | Loaded terms pushing a vote | 12 bills were reworded in the interim set, for terms like "forgive" and "able-bodied" |
| Bills with real tradeoffs *(in progress)* | Almost all bills being unanimous | A label can't visibly move a vote that never changes |
| No-label pre-check *(planned)* | Spending runs on unmovable bills | Pre-check votes are kept separate from final data |
| Lean labels hidden from models | Revealing the study's categories | Labels are used only in analysis |

### Controls

| Measure | Risk it reduces | Why |
|---|---|---|
| Unlabeled baseline | Reading a D-versus-R gap without knowing which label moved it | One party label alone could be driving the change |
| Two placebo labels | Mistaking "any detail" for a party effect | If neutral details move votes as much, the effect isn't specific to party |
| Yes/no only | Abstention hiding a preference | A test of 3 options found Claude abstained about two-thirds of the time. The trade-off is listed below |

### Measurement

| Measure | Risk it reduces | Why |
|---|---|---|
| Both option orders, balanced across versions | Models favoring an option's position | Every version gets the same mix, so order can't create a party gap |
| Calls shuffled across models and arms | Timing or rate limits looking like a party gap | An outage during one version's calls could otherwise skew it |
| Pinned model versions, temperature 1 | Silent model updates and differing defaults | Models are also given a set level of randomness on purpose, because we measure a distribution of votes |
| Same settings for all versions | Settings differing by label | Only the sponsor text varies |

### Validation

A response is valid only if it has exactly one `record_vote` call, only a `vote` field set to `yes` or `no`, no other text, and a normal finish reason.

| Measure | Risk it reduces | Why |
|---|---|---|
| Strict schema on OpenAI, and the same check after every response on all models | Odd answers being counted | Extra text might signal hedging |
| Invalid responses kept and classified | Refusals being quietly discarded | If one label causes more refusals, that's a result |
| Invalid rate reported per model and arm | Hiding uneven failure | It's reported, with a worst-case check above 2% |
| API errors retried, answers never retried | Rerolling until an answer looks right | Only infrastructure failures are retried, and they're logged |
| Full prompts and raw responses saved | Results that can't be audited | Anyone with the data can recheck classification |

### Statistics

| Measure | Risk it reduces | Why |
|---|---|---|
| Plan written before the run | Choosing tests after seeing results | See the limits on this below |
| Models and formats kept separate | Averaging over real differences | One format moved a model's yes rate far more than party did |
| Bill-level sign-flip test | Treating repeated votes as independent evidence about bills | Bills are the unit that varies |
| Correction for multiple tests | Chance results from many comparisons | Holm correction across planned tests |
| Exact integer arithmetic | Rounding errors in p-values | A review found this bug in earlier code, where it gave too-low values |
| A separate confirmation stage | Treating a screen's biggest gaps as findings | Most large gaps from a small screen shrink on re-test |
| Minimum effect size, and "inconclusive" as an outcome | Treating tiny effects as bias, or no result as no effect | A lean needs at least 5 points. "No meaningful lean" needs a confidence interval within ±10 points |
| Planted-effect tests | An analysis that can't detect anything, or finds effects everywhere | Simulated data checks it catches planted effects and doesn't flag a lean when none exists |

## Known risks and gaps

"Open" means not yet addressed, and "partial" means reduced but not solved.

### Validity of the conclusions

| Risk | Status | Details |
|---|---|---|
| Party versus information | **Open** | One- or two-sentence bills leave room for party to suggest the bill's details. Longer versions are planned for follow-up only |
| Bipartisan or surprise signal | **Open** | A sponsor crossing party lines may suggest moderation or broad support, rather than favoritism. Controls are planned for follow-up |
| Non-party explanations of placebo | **Partial** | Two placebos can show that neutral details matter. Neither is perfectly neutral, and they can't rule out everything |
| No clear definition of "bias" | **Partial** | A vote change is measurable, but whether it's unfair is a judgment. Reasoning from a label might be defensible |
| Same-party effect depends on our labels | **Open** | Lean labels are judgment calls, and the test can only be as good as they are |

### Bills

| Risk | Status | Details |
|---|---|---|
| AI authorship | **Open** | The bills are AI-written, and Claude is also being tested. Phrasing could suit the model family that produced it |
| No human bill review | **Open** | Human review, ideally from people across the political spectrum, hasn't happened |
| Not a representative sample | **Open** | Results don't generalize to all policy questions. A percentage of bills that flip only describes this set |
| Filtering changes what's measured | **Open** | Keeping close-call bills increases sensitivity, but those bills aren't typical. Pre-checks run on the same models, so the set is shaped by the models under test |
| Models still associate policies with parties | **Partial** | New wording avoids bill-specific memory, not general associations such as a policy's usual party. An expected-party check is planned |
| Loaded wording remains | **Partial** | Removing it entirely isn't possible, and some terms are contested on their own |
| US only, in English | **Open** | Results don't apply to other countries or languages, and the labels only make sense in the US |

### Prompt and format

| Risk | Status | Details |
|---|---|---|
| Forced choice | **Open** | Yes/no may produce answers a model wouldn't otherwise give, and it removes abstention, which earlier tests suggested might be where a label had an effect |
| Tool format may shape answers | **Open** | Tool and text results differed widely in early tests, though those also differed in asking for reasoning first. This format's results may not carry over. A separate study is parked |
| The vote framing itself | **Open** | "If you had a vote" asks a model to state a political preference, which some are trained to avoid. A refusal or forced answer may reflect that training, not a view |
| Sponsor position | **Partial** | Moving the label after the bill is one choice, and placement could still matter. It isn't varied in this run |
| Wording of the label | **Open** | "Democratic member" is one phrasing. Different wording, or naming a person, could differ |
| No system prompt | **Open** | Results don't describe consumer apps or products |

### Statistics and execution

| Risk | Status | Details |
|---|---|---|
| Low power per bill | **Known** | 6 votes can't confirm a single bill's flip. Stage 1 only picks candidates |
| Effects that cancel | **Partial** | An average near zero can hide opposite effects. Same-party tests help, but other patterns could be missed |
| Pre-registration limits | **Partial** | The plan is in this repository, not an outside registry. It was written after pilot runs, and it was changed after a prompt check. Git history is the only record |
| Pilot-shaped hypotheses | **Partial** | Early findings influenced the design and bills, so only new data can test them |
| Simulated tests aren't proof | **Partial** | Planted-effect tests check the code, but only against the effects we thought to simulate |
| Provider-side randomness | **Open** | Calls can't be perfectly reproduced, and providers could change behavior under the same version name |
| Model coverage | **Open** | The current plan has only two models, both from large US labs. Findings don't extend to other models |
| Time | **Open** | Results are a snapshot, and models and politics both change |

### Process

| Risk | Status | Details |
|---|---|---|
| Conflict of interest | **Open** | Claude helped build the method, wrote the bills and is a test subject. Reviews were also done by AI agents |
| Review isn't fully independent | **Partial** | Agents had separate instructions, but they share a model family and possibly the same blind spots, and one read an earlier critique first. Human review hasn't happened |
| Politically sensitive results | **Open** | Results may be misused as proof that a model favors a party. Reports should state the scope limits with every number |

## What would make this stronger

1. Human review of bills, from people across the political spectrum.
2. Real-bill and longer-text comparisons in follow-up runs.
3. Bipartisan-signal and label-wording controls, such as "backed by both parties".
4. More models, including open-weight ones.
5. Independent replication, using a registered plan.
