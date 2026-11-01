# Methodology

This explains how partisan-cue-bench tries to reduce bias, why each choice was made, and what could still be wrong. It covers the current design. The analysis rules are in the [pre-registered plan](PREREGISTRATION.md). This design replaced an earlier pilot after reviews found problems with its role-play framing, metrics, abstain option and statistics.

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
| Plainer wording | Loaded terms pushing a vote | An agent audit edited 172 of 200 bills for sourced-sounding claims, loaded language and similarity to real bills. See [the change log](../data/candidates_audit.md) |
| Bills with real tradeoffs | Few bills being close calls | Most bills were still unanimous in the pre-check, as noted in the risks below |
| No-label pre-check | Spending runs on unmovable bills | Pre-check votes are kept separate from final data |
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
| Models named, settings and returned versions logged | Silent model updates and differing defaults | Neither current model is a dated snapshot, so returned names and reasoning tokens are saved. Claude runs at temperature 1. `gpt-6.1-sol` uses its default settings. Votes turned out nearly deterministic for both models, and for Claude most variation came from option order |
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
| Stated costs and benefits may steer votes | **Open** | Many bills state effects, and those choices are subjective. Finding 1 could partly reflect them, so a version without stated effects is a planned test |
| Few close calls | **Open** | Only 5 of 192 bills were split for `gpt-6.1-sol` and 10 for `claude-opus-5` with no label. This limits sensitivity, and the selection rule favored bills the models disagree on |

### Bills

| Risk | Status | Details |
|---|---|---|
| No neutral author | **Partial** | Every author has a bias. The bills are AI-written, and Claude is also being tested, so phrasing could suit that model family. A human author would bring different biases, not none. Using identical text across sponsor versions limits the effect, because wording can't by itself create a gap between versions, though it can still affect which bills are able to move and how a label reads |
| One-sided review | **Open** | Only AI agents have reviewed the bills. No single reviewer can settle this, human or AI. The goal is to expose biases by comparing reviewers with different views, and by checking results across different bill authors |
| Not a representative sample | **Open** | Results don't generalize to all policy questions. A percentage of bills that flip only describes this set |
| Filtering changes what's measured | **Open** | The current selection rule mostly picks bills the two models disagree on, not true close calls, and it should be replaced before the main run. Pre-checks run on the same models, so the set is shaped by the models under test |
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
| Newest Claude models excluded | **Open** | `claude-opus-5-5` and `claude-sonnet-5-5` don't accept a required tool call, and they declined to vote in nearly every plain one-word test. Results don't describe them. Whether a label changes their refusals is a separate later question |
| Reasoning differs between models | **Open** | `gpt-6.1-sol` reasons by default, and `claude-opus-5` showed no reasoning with a required tool. Any model difference could partly reflect that, so models shouldn't be ranked against each other. Low-versus-high reasoning tests are planned for follow-up |

### Statistics and execution

| Risk | Status | Details |
|---|---|---|
| Low power per bill | **Known** | 6 votes can't confirm a single bill's flip. Stage 1 only picks candidates |
| Effects that cancel | **Partial** | An average near zero can hide opposite effects. Same-party tests help, but other patterns could be missed |
| Pre-registration limits | **Partial** | The plan is in this repository, not an outside registry. It was written after pilot runs, and it was changed after a prompt check. Git history is the only record |
| Pilot-shaped hypotheses | **Partial** | Early findings influenced the design and bills, so only new data can test them |
| Simulated tests aren't proof | **Partial** | Planted-effect tests check the code, but only against the effects we thought to simulate. They don't yet cover nearly deterministic votes |
| Floors and ceilings | **Open** | With a model already at 0% or nearly 100% on many bills, a party label has little visible room to move votes, and that can hide an effect or fake a direction. The analysis needs to be split by lean and baseline before the main run |
| Missing or invalid votes | **Open** | The current analysis counts them as no, and doesn't check for missing rows. This must be fixed before the main run |
| Provider-side randomness | **Open** | Calls can't be perfectly reproduced, and providers could change behavior under the same version name |
| OpenRouter hosts | **Partial** | Runs can pin one host, disable fallbacks and record what ran. Hosts can still differ in version or filtering, so results describe that host. Finding 4 reports `z-ai/glm-5.3` on Wafer and `x-ai/grok-4.3` on xAI |
| Model coverage | **Open** | The planned analysis covers two models from large US labs, and Finding 4 adds one Chinese model and one older Grok release. None is pinned to a dated snapshot, and findings don't extend to other models |
| Time | **Open** | Results are a snapshot, and models and politics both change |

### Process

| Risk | Status | Details |
|---|---|---|
| Conflict of interest | **Open** | Claude helped build the method, wrote the bills and is a test subject. Reviews were also done by AI agents |
| Review isn't fully independent | **Partial** | Agents had separate instructions, but they share a model family and possibly the same blind spots, and one read an earlier critique first. Human reviewers would add different blind spots, and haven't been used yet |
| Politically sensitive results | **Open** | Results may be misused as proof that a model favors a party. Reports should state the scope limits with every number |

## What would make this stronger

1. Bills from several kinds of authors, including other AI models and people across the political spectrum, with results compared by author. Agreement across authors would be stronger evidence than trusting any one of them.
2. Real-bill and longer-text comparisons in follow-up runs.
3. Bipartisan-signal and label-wording controls, such as "backed by both parties".
4. More models, including open-weight ones.
5. Independent replication, using a registered plan.
