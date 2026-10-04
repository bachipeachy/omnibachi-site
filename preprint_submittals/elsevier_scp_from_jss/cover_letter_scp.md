Bhash Ganti · Independent Researcher, Camas, WA, USA · ORCID 0009-0007-3810-6520 · omnibachi.org

To the Editors, Science of Computer Programming

Re: Submission — "Protocol-Governed Computing: A Software Development Lifecycle Architecture for Deterministic Declarative Execution and Governed Transformation"

Dear Editors,

I submit the manuscript above for consideration as a Research Paper. It reaches you through Elsevier's transfer service from the Journal of Systems and Software (JSSOFTWARE-D-26-02392); as the transfer registered without content, I am submitting it afresh.

**What the paper is about.** Software behavior is rarely determined in one place. Some is stated in declarations; some is supplied by build tooling, runtime defaults, environment discovery, or fallback behavior. The paper treats this as a question of where behavioral authority resides across the lifecycle, and presents an architecture in which one semantic schema governs all three activities: transformation determines the next declarations from a named predecessor, construction determines whether candidate declarations may exist and emits a sealed snapshot, and execution realizes that snapshot without adding behavioral authority. Each transition produces evidence; a refused transition produces no usable governed result. The architecture is then reduced to a compact set of checkable conformance obligations and assessed against a named, publicly deposited reference realization.

**Why Science of Computer Programming.** SCP's scope covers methods for the entire life cycle of software systems, and this paper's subject is that life cycle taken as one governed object rather than as separate phases. Its contribution sits in the journal's experimental and descriptive lines of work rather than its formal one.

The distinction matters for how the paper should be read. Its normative apparatus — the specification family the architecture is defined by — is deposited separately and cited, not developed here. What this paper contributes is the architecture, a conformance view derived from it, and an assessment of an executable realization against that view. The realization is a working toolchain: a compiler, a snapshot assembler, a runtime, an inspector, a transformation toolchain, and domain workloads. The composition assessed is deposited with a DOI and identified by a content-derived snapshot identity, and the manuscript carries a reproduction record by which a reader regenerates that identity from the named revision. The empirical portion is therefore open to inspection rather than asserted, and the results reported include the ones that do not support the architecture.

The paper is bounded in the way this readership expects. It separates what the architecture requires, what the specification makes normative, what the implementation was observed to do, and what the evidence establishes, and it names the claims the evidence does not support. Checks that are red by design or advisory are reported as such rather than resolved into a binary maturity claim.

**What is novel.** The lifecycle composition itself is a synthesis of prior deposited work, and the paper says so. The novel contributions are: unifying governed transformation, governed construction, and deterministic execution under a single predecessor-to-successor transition while preserving the distinct authority of each; deriving a compact conformance view — closure, reachability, inspection, refusal, evidence, externally authored profiles — from that composition; and, most importantly, a discipline of claim separation that prevents the presence of a governance mechanism from standing in for evidence that the mechanism secures the property it was built for.

I am an independent researcher writing from more than forty years in large-systems integration as a systems architect. The problem addressed here is one I met repeatedly in practice long before it had a name: systems that work while no single artifact determines what they may do. That vantage is what the paper contributes in place of a laboratory.

**Affiliation.** I hold no institutional affiliation of any kind. My research is published under my own name at omnibachi.org, which is my research website and the only body I am associated with. Correspondence should be directed to me personally.

The manuscript is original, is not under consideration elsewhere, and has not been published previously. A companion study by the same author, cited in §1.3 for disclosure, is under concurrent review elsewhere; it addresses a different question and reuses no text, argument, or evidence from this paper. Prior PGC preprints synthesized here are deposited and cited by DOI. There is no funding and no conflict of interest. Use of a generative AI assistant is disclosed in the manuscript.

Thank you for your consideration.

Sincerely,

Bhash Ganti
