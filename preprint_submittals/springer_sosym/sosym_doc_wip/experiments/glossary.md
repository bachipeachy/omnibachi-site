# Glossary

**Acceptance.** The check a runtime makes before execution. It establishes integrity, identity, totality and the profile claim. If any fails, the runtime refuses the whole snapshot.

**Behavioral authority.** A model holds behavioral authority over a decision when two conditions hold. Declarations in the model determine the decision. Every downstream stage is barred from supplying a different determination.

**Captured input.** A non-deterministic result that the runtime records once. Replay substitutes it. A deterministic step must judge it before any route depends on it.

**Construction.** The activity that admits or refuses candidate declarations and seals the admitted ones into a snapshot.

**Determination.** A decision about what the system is authorized to do. The sealed model holds it.

**Domain-visible behavior.** Decisions in six classes: admission, outcome, route, effect, event and captured input.

**Explain.** A read-only query that joins one trace to its sealed model. It attributes each recorded decision to a declaration and keeps recorded facts apart from joined facts.

**Governing closure.** The complete set of governing elements that apply to a declaration, with their authority and scope.

**Named predecessor.** The sealed snapshot that a change builds on, identified by its content hash.

**Observation.** A record of what one execution did. The trace holds it.

**Profile.** An external constraint that a snapshot claims. The snapshot does not author it.

**Realization.** The work of turning authorized behavior into running machinery. Construction and the runtime perform it.

**Refusal.** A determination that nothing proceeds, with recorded grounds. A declared "rejected" outcome is a route, not a refusal.

**Snapshot.** A sealed, complete, self-identifying, self-describing and verifiable composition of declarations.

**Supersession.** A declared relation between two exact identities. A successor stands in for a predecessor, and references to the predecessor keep their meaning.
