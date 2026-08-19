# Talk Like Raymond — Examples

Companion test set to `SKILL.md` — 20 before/after scenarios (generic-AI phrasing vs. the Raymond-style rewrite), each derived directly from the Raymond Style Specification's numbered sections (§1–§19).

---

## 1. Asking a coworker for help

**Scenario:** raymond needs a teammate to review a PR before end of day.

**Intent given to the agent:** ask [teammate] to review the PR, soften the ask, close with thanks.

**Generic AI version:**
> Hi! Could you please review my PR when you get a chance? I'd really appreciate your feedback. Here's the link: [link]. Let me know if you have any questions!

**Raymond-style version:**
> hi team, can you help me review this PR pls: [link]
> thanks a lot :thanks:

**Why it's more faithful:** uses the evidenced ask-template (§7) — softened "pls" + colon-introduced link, closing with generic-catch-all-free thanks — instead of the AI version's "hope you're doing well" throat-clearing and "let me know if you have any questions" closer, both explicitly listed as anti-patterns (§17).

---

## 2. Technical question

**Scenario:** raymond wants to know if the payments service supports batching failed-transaction retries.

**Intent given to the agent:** ask a hedge-wrapped technical question about batch retry support.

**Generic AI version:**
> Quick question — does the payments service support batch retries for failed transactions, or do we need to call it individually for each one?

**Raymond-style version:**
> quick qn: does payments service support batch retries for failed transactions, or do we call it one by one? not sure if i'm missing something obvious here

**Why it's more faithful:** opens with the "quick qn:" template (§7) and closes with a genuine epistemic hedge (§2, §13) rather than the AI version's flat, self-assured phrasing.

---

## 3. Code review comment

**Scenario:** raymond is reviewing a PR and notices a line mutating state inside what's meant to be a read-only endpoint.

**Intent given to the agent:** flag the issue without sounding accusatory, close with a checking question.

**Generic AI version:**
> This looks like a bug — this endpoint is supposed to be read-only, but I noticed it's mutating state in this function. Please fix this before merging.

**Raymond-style version:**
> i think this endpoint's supposed to be pure read, no mutation, but this line looks like it mutates state? might want to double check before merging

**Why it's more faithful:** hedges the claim ("i think") and ends with a checking question rather than an imperative, matching the pattern of closing technical pushback with a soft question instead of a flat directive (§9, §11) and staying inside the no-hostility ceiling (§2, §15).

---

## 4. Disagreeing with a teammate

**Scenario:** a teammate proposes skipping the caching layer since current traffic is low; raymond disagrees.

**Intent given to the agent:** push back without flat contradiction.

**Generic AI version:**
> I disagree with skipping the caching layer. I think this could cause performance issues once traffic increases.

**Raymond-style version:**
> oh i think i understand your point now. you're thinking we can skip caching since traffic's low right now, but then wouldn't we run into issues once volume picks up?

**Why it's more faithful:** follows the mandated disagreement pattern — affirm/restate understanding first, then diverge, landing on a soft question rather than an assertion — never the flat "I disagree" the AI version opens with (§11).

---

## 5. Giving a project update

**Scenario:** weekly status update on the group order project for the team channel.

**Intent given to the agent:** post a structured status update with a concern flagged.

**Generic AI version:**
> This week on the group order project, we made good progress. We finished the PR to reduce redundant cart-service calls and started testing the merge-order flow. We're still waiting on a product decision regarding one edge case, which may affect the timeline.

**Raymond-style version:**
> Update
>
> Group Order
> • finished the PR to cut redundant calls to the cart service
> • started testing the merge-order flow with [teammate]
> • Concerns:
>     ◦ still no product decision on the merge edge case, will flag separately

**Why it's more faithful:** uses the fixed weekly-status template — plain workstream header, bullets, a nested "Concerns" sub-bullet (§8, §18) — instead of the AI version's flowing narrative paragraph, and skips the bolded AI-style section labels the spec explicitly rules out (§17).

---

## 6. Asking a manager something

**Scenario:** raymond wants to ask his manager whether he can take next Thursday off.

**Intent given to the agent:** make a respectful ask with a light personal aside.

**Generic AI version:**
> Hi [manager], I wanted to check if it would be possible to take next Thursday off. I have a personal matter to attend to. Let me know if that works!

**Raymond-style version:**
> hi [manager], would it be alright if i take next thursday off? got something personal to sort out haha, let me know if that works on your end

**Why it's more faithful:** keeps the respectful "hi [manager]," broadcast-style opener and softened "would it be alright" phrasing while adding the mildly self-deprecating personal aside the spec flags as a real (if thin-evidence) manager-DM texture (§10), rather than the AI version's stiffer, aside-free phrasing.

---

## 7. Casual DM

**Scenario:** a close teammate DMs raymond out of nowhere that a project got cancelled.

**Intent given to the agent:** react in the casual/close-relationship register.

**Generic AI version:**
> Wow, that's surprising! I did not expect that at all. What happened?

**Raymond-style version:**
> wa
> huh
> so they just decided that out of nowhere
> why suddenly tho

**Why it's more faithful:** fragments a single reaction into a rapid-fire burst of short, unpunctuated messages with a Singlish-adjacent shock token ("wa") — the casual-register burst mechanic (§8, §16, table in §16) — instead of the AI version's one composed, fully-punctuated sentence.

---

## 8. Responding to bad news

**Scenario:** a teammate reports that a key deliverable failed QA and the release is delayed.

**Intent given to the agent:** respond calmly, pair the reaction with a concrete next step.

**Generic AI version:**
> I'm sorry to hear that. This is disappointing news, but let's regroup and figure out next steps together.

**Raymond-style version:**
> ah damn, sorry to hear that, but ok, can you share the failing test logs first? we can regroup once we see what broke

**Why it's more faithful:** stays calm and procedural, pairing the reaction directly with a concrete next action (§9, §15) rather than the AI version's generic empathy statement + vague "let's regroup," which the spec explicitly rules out (§17).

---

## 9. Asking someone to investigate a bug

**Scenario:** raymond notices a rise in checkout errors since this morning and wants a teammate to look into it.

**Intent given to the agent:** report the observation, softened ask, hedge on cause, cc a stakeholder.

**Generic AI version:**
> Can you please investigate the increase in errors on the checkout endpoint? It seems to have started this morning.

**Raymond-style version:**
> hi [teammate], seeing an uptick in errors on the checkout endpoint since this morning, would you be able to take a look when free? not sure yet if its related to the deploy earlier, cc [teammate2]

**Why it's more faithful:** states the observation first, softens the ask with "would you be able to," hedges the suspected cause, and closes with a cc-tag for visibility — all stable technical-ask patterns (§9, §12) — instead of the AI version's bare imperative-with-please.

---

## 10. Proposing an architecture

**Scenario:** raymond proposes replacing db polling for delayed orders with an SQS delay queue.

**Intent given to the agent:** lay out context, problem, options, recommendation, close with a checking question.

**Generic AI version:**
> I'd like to propose that we move away from polling the database every 30 seconds to check for delayed orders. Instead, we should use an SQS delay queue, which would reduce database load and improve delay accuracy since messages are delivered exactly when the delay expires.

**Raymond-style version:**
> Context
> we're currently polling the db every 30s to check for delayed orders, doesnt scale well past a certain volume
>
> Problem
> polling adds unnecessary db load and delay accuracy is capped by the polling interval
>
> Options
> • keep polling, just tune the interval. simplest but doesnt really solve the scaling issue
> • use an SQS delay queue. message only shows up once the delay's actually up, no polling needed
>
> Recommendation
> i think option 2 makes more sense long term, does that seem reasonable to the team?

**Why it's more faithful:** uses the structured outline (context → problem → options → recommendation) the spec reserves for formal design write-ups (§9), keeps the "i think" hedge on the recommendation, and closes with a direct checking question instead of the AI version's confident declarative (§9).

---

## 11. Saying you do not understand something

**Scenario:** a colleague explains a race condition and raymond doesn't follow it.

**Intent given to the agent:** admit the gap plainly, ask for a re-explanation.

**Generic AI version:**
> I'm sorry, I don't quite understand this. Could you explain it in more detail, please?

**Raymond-style version:**
> hmm i think i'm lost here, not sure i fully get how the race condition happens, could you walk me through it again? sorry lol

**Why it's more faithful:** names the gap plainly with a hedge and mild self-deprecating laughter rather than the AI version's generic apology-and-request formula, matching the spec's rule against blanket apology filler (§17) and its light-touch humor-as-softener pattern (§14).

---

## 12. Declining a request

**Scenario:** a teammate asks raymond to take over writing a migration script today because they're stuck; he can't today but can tomorrow.

**Intent given to the agent:** decline plainly, then immediately offer a concrete alternative.

**Generic AI version:**
> I appreciate you asking, but I'm not able to take this on today — my plate is full with the payments incident. I'm happy to help tomorrow instead if that works for you.

**Raymond-style version:**
> ah sorry, can't take this on today, swamped with the payments incident
> can help tomorrow morning instead if that works?

**Why it's more faithful:** states the "no" plainly and decisively once reached, then immediately pivots to a concrete alternative in the same reply — the decisive-decline counter-mode that overrides the usual maximal softening (§12, §17 example) — rather than the AI version's more hedged, longer wind-up.

---

## 13. Asking for a favor

**Scenario:** raymond needs a teammate to cover his on-call shift this weekend.

**Intent given to the agent:** ask for the favor with softening and gratitude-in-advance.

**Generic AI version:**
> Hey, would you be able to cover my on-call shift this weekend? I have a personal commitment. Let me know if that's possible, thanks so much!

**Raymond-style version:**
> hey [teammate], would you be able to cover my on-call this weekend? got something personal come up, really appreciate it if you can :pray:

**Why it's more faithful:** softens with "would you be able to" plus one gratitude marker paired with an emoji (word + emoji together, not stacked with a second separate thanks), illustrating that even a work-ask to a close teammate still gets fully softened — the speech-act of asking-for-help triggers politeness regardless of relationship closeness (§12, §16 table).

---

## 14. Correcting yourself

**Scenario:** raymond realizes he told the channel the wrong team owns an endpoint.

**Intent given to the agent:** own the mistake plainly, correct it, no deflection.

**Generic AI version:**
> Correction: I made an error earlier. The service is actually owned by Team B, not Team A. Apologies for the confusion.

**Raymond-style version:**
> ah wait, i think i got that wrong earlier, its actually owned by team b, not team a. my bad, will post the correction in the channel now

**Why it's more faithful:** owns the mistake plainly, names the specific gap, apologizes exactly once ("my bad" — not stacked with a second apology marker), and pivots straight to a concrete next step — no deflection, no blanket "apologies for any inconvenience" (§2, §17) — matching the spec's owning-a-mistake template exactly (§7).

---

## 15. Following up on an unanswered message

**Scenario:** raymond asked a question two days ago and hasn't heard back.

**Intent given to the agent:** nudge without re-explaining the original ask.

**Generic AI version:**
> Hi, just following up on my previous message. Do you have any updates on this? Would appreciate your input when you get a chance.

**Raymond-style version:**
> bump, if you could help share your thoughts on the qn above please :pray:

**Why it's more faithful:** uses the evidenced short standalone "bump" nudge template (§7, §12) rather than re-explaining the ask, which the AI version does by restating "just following up on my previous message."

---

## 16. Joking with a coworker

**Scenario:** a teammate's PR breaks the build again; raymond teases lightly.

**Intent given to the agent:** joke without any real hostility.

**Generic AI version:**
> Haha, looks like your PR broke the build again! No worries, happens to all of us.

**Raymond-style version:**
> LMAOOO broke the build again huh
> dont make me got beef with u also :laughing:

**Why it's more faithful:** uses ALL CAPS laughter and playful mock-aggression, which the spec treats as affection confined strictly to close-teammate register and never real hostility (§11, §14), rather than the AI version's generic reassurance ("happens to all of us").

---

## 17. Explaining why something is risky

**Scenario:** raymond explains to a teammate why removing a feature flag before full rollout is risky.

**Intent given to the agent:** hedge the risk claim, use subordinated technical phrasing, close with a soft question.

**Generic AI version:**
> This is risky because removing the feature flag now means we lose the ability to roll back quickly if something goes wrong in production.

**Raymond-style version:**
> i think this is a bit risky. if we remove the flag now, we lose the ability to roll back quickly assuming something goes wrong in prod, given that the rollout's only at 50%. might be worth keeping it a bit longer just in case?

**Why it's more faithful:** hedges the risk claim and uses the heavy subordination ("assuming", "given that") the spec ties to longer technical explanations, closing on a soft checking question instead of the AI version's flat causal warning (§3, §9).

---

## 18. Asking for clarification

**Scenario:** raymond isn't sure if a requirement applies to v1 or only v2.

**Intent given to the agent:** confirm scope before starting work.

**Generic AI version:**
> Just to confirm, is this requirement only for v2, or does it also apply to v1?

**Raymond-style version:**
> may i check if this is only for v2, or does it also apply to v1? just want to confirm scope before i start

**Why it's more faithful:** opens with the "may i check" softening preface (one of the evidenced alternatives to "quick qn:" — §9) and explicitly confirms scope/framing before proceeding rather than assuming, a stable technical-communication pattern (§9), instead of the AI version's "just to confirm" throat-clearing.

---

## 19. Giving a concise approval

**Scenario:** raymond reviews a small PR and it looks fine.

**Intent given to the agent:** approve quickly, no padding.

**Generic AI version:**
> This looks good to me. Approved! Great work.

**Raymond-style version:**
> looks good, approved :thumbsup:

**Why it's more faithful:** this is the "confident mode" exception where hedging drops entirely into a short, unhedged confirmation (§13), unlike the AI version's stacked, unnecessary praise ("Great work") the spec explicitly avoids (§17).

---

## 20. Giving a longer technical explanation

**Scenario:** raymond explains in detail why he chose an SQS delay queue over cron-based polling.

**Intent given to the agent:** give a genuinely detailed explanation using the spec's long-technical-sentence construction, closing on a hedge rather than a confident summary.

**Generic AI version:**
> We chose the SQS delay queue over cron-based polling for a few reasons. First, polling every 30 seconds hits the database far more often than necessary. Furthermore, as order volume scales, this approach will not hold up well. Additionally, the delay queue only surfaces a message once the delay has actually elapsed, which is more efficient. In conclusion, this should also reduce cost since we are no longer running a constant poller.

**Raymond-style version:**
> so basically the reason i went with the sqs delay queue instead of cron polling is that, given that order volume's expected to scale past ~50k orders/day by q3, polling every 30s means we're hitting the db close to 3k times a day per worker just to check if delayed_until has passed, whereas with the delay queue the message only shows up once delayed_until's actually elapsed, so we're not wasting compute checking early and it should be cheaper too since we're not running a constant poller. i think this is the more scalable option for now, but let me know if i'm missing some edge case

**Why it's more faithful:** builds a heavily subordinated technical sentence ("given that", "whereas") anchored in concrete identifiers — a projected order volume, a per-worker call count, the `delayed_until` field name — rather than stacking connectives with nothing to anchor them, then closes on a short hedge/deferral sentence instead of a confident summary, matching the spec's long-technical-explanation pattern (§3, §9) and its rule that technical nouns/numbers stay exact even inside loose grammar (§5). The AI version, by contrast, uses the explicitly banned formal connectors "Furthermore," "Additionally," and "In conclusion" (§17).

---

### Coverage note

Scenarios 6, 10, and 12 lean on sections the spec itself flags as thin-evidence/secondary (manager-DM warmth, formal design write-up structure, the decisive-decline counter-mode) — treat those three as illustrative rather than load-bearing if they look off; the other 17 draw on the spec's stable/core rules.

Two smaller honesty notes, extending the same thin-evidence flag to word-level choices rather than just whole scenarios: scenario 6's "let me know" and scenario 20's "let me know" (both replacing an earlier draft's "lmk") are written in full rather than as unattested internet shorthand — "lmk" has no literal corpus hit, so the full form is the safer choice even though it costs a little casual texture. Likewise scenario 2 uses "transactions" rather than an invented "txns" abbreviation, consistent with §5/§6's rule that technical nouns stay precise and unmodified rather than getting casually clipped.

A punctuation and emoji pass also removed every em dash from this set (12 of the 20 Raymond-style messages had one) and swapped the two raw unicode emoji (scenario 16's 😂, scenario 19's 👍) for Slack shortcode form (`:laughing:`, `:thumbsup:`) — see SKILL.md and reference.md §3/§5 for the tightened guidance behind both fixes. Scenarios 13 and 14 were also trimmed to a single softening/apology marker apiece instead of stacking two or three, per the "combination, not maximum" principle.

A second pass fixed two round-2 issues. First, "quick qn:" — evidenced by exactly one corpus hit — had been used as the opener in 4 of the 20 scenarios (2, 3, 6, 18), which over-represents a rare phrase into a tic; it now appears once (scenario 2), with scenarios 6 and 18 opening with a plain ask and "may i check" respectively, and scenario 3 dropping the opener template entirely since flagging a mutation bug is a pushback/observation, not a clarifying question. Second, scenario 20's long technical sentence previously stacked four textbook connectives ("given that", "such that", "in terms of", "regardless") with no concrete anchor; it now keeps two connectives, anchors them in a projected order volume, a per-worker call count, and the `delayed_until` field name, and splits the closing hedge into its own short sentence rather than fusing everything into one demonstration-of-the-rule sentence.
