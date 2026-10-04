| **Bhash Ganti**
| Independent Researcher, Unaffiliated
| Camas, WA 98607, United States
| bachipeachy@gmail.com
| ORCID 0009-0007-3810-6520

To the Editors-in-Chief
*Automated Software Engineering*

**Re: Submission — "Protocol-Governed Human–AI Software Engineering: Autonomy Without Authority"**

Dear Editors,

**Context.** Automation has reached the point where an agent can carry out most of a software
lifecycle: draft requirements, derive a design, write the implementation and tests, and open the
change that puts them into a running system. What has not moved is the authorization decision. It
still rests at human review, where approval carries two claims at once — that the code is
correct, and that it may run. Those travelled together when one small group wrote, reviewed and
operated a system; as the producer changes, they come apart. Write access, signed commits, attested
builds and admission policies each establish something real, but none establishes that the resulting
behaviour is permitted.

**Importance.** The paper separates **activity autonomy** — who may analyze, design, construct and
transform — from **authorization authority** — who may set scope, admit a candidate and promote it as
the next executable baseline — and asks what remains of the second when an agent performs the first.
The answer it examines is architectural rather than procedural: behaviour is determined during
governed construction and sealed into state that execution realizes but cannot amend. The claim is
evaluated against a working realization of nine declared phases and seven governed domains, exercised
through one complete agent-mediated transformation, with each boundary reported at the rung its
evidence supports and unexercised boundaries reported as declared rather than observed.

One finding runs against the paper's own interest, and I would rather it were read than found. A
mutation study asked whether the demonstrations offered as governance evidence would fail if the
guards they tested were removed; two of six did not. The guards were present and required — the
evidence for them did not discriminate. The result is evidentiary and transferable: a property can be
specified, implemented and reachable, and be asserted about in a demonstration that passes without
ever showing the guard was necessary.

**Fit to the journal.** The work is about what automating the lifecycle does to the lifecycle's own
control structure, evaluated on a running implementation rather than argued from a design — which is
the kind of contribution this journal publishes. It also engages directly with recent work in these
pages on the reliability of LLM judgement in conformance review (Jin and Chen, *Autom. Softw. Eng.*
33(3), 2026). That literature asks how to make the judgement better; this paper asks how much should
depend on it, and is a complementary rather than competing response.

I am an independent researcher with no institutional affiliation, writing from more than forty years
in large-systems integration as a systems architect. There is no funding and no conflict of interest.
The manuscript is posted as a preprint at <https://doi.org/10.5281/zenodo.22650863>, per Springer
Nature's preprint policy; the reference implementation is archived under Apache-2.0 with URLs, commit
identities and DOIs in Appendix A.6; and Section 3.3 discloses the author's use of AI tools and states
that no model is an author. Should length be a constraint, I am glad for the article to be considered
for a regular issue rather than a special issue. The manuscript is original, is not under
consideration elsewhere, and has not been published previously.

Sincerely,

Bhash Ganti
