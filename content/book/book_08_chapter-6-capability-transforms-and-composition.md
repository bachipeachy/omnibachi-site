---
title: Chapter 6 — Capability Transforms and Composition
date: '2026-03-05'
draft: false
weight: 8
slug: chapter-6-capability-transforms-and-composition
---

Chapter 5 executed the User Registration workflow as a DAG traversal. When the engine reached a CT_ step inside a capability contract, it dispatched to a transform and received a result. The transform was a black box --- the engine sent inputs in and got outputs back. It did not know what happened inside. It followed the edge.

This chapter opens the box. It answers: **How does pure computation work inside a protocol-governed system --- and how do small, single-purpose functions compose into complex pipelines without losing determinism or governance?**

The CT_ layer is where PGS delivers on a promise that object-oriented programming made but could not structurally sustain: genuine, governed reuse. An atom is a pure function --- no side effects, no state, no I/O. Given the same inputs, it always produces the same outputs. Atoms compose into molecules through explicit dataflow declarations, not inheritance hierarchies or dependency injection. The chapter shows how atoms are defined, how molecules compose them, and how CT-IR (the intermediate representation) normalizes both into the uniform execution format that the transform executor consumes. By the end, the reader will understand why the same atom that generates a user ID also generates a wallet ID, a transaction ID, or any other deterministic identifier --- without modification, without subclassing, without configuration.

## 6.1 --- The Engineering Objective

Chapter 5 dispatched to CT_ steps as black boxes. When CC_GENERATE_USER_ID_V0 executed, the engine sent inputs to a transform and received a result. The engine did not know --- and could not know --- what happened inside. It followed the edge.

This chapter opens the box.

**The Task:** Examine how pure computation executes inside a capability contract --- how atoms are defined, how molecules compose atoms, and how CT-IR normalizes both into a uniform execution format.

**The Constraint:** No side effects. A CT_ atom cannot write to a database, call an API, read a file, access a clock, or mutate any state outside its declared outputs. Given identical inputs, it must produce identical outputs --- always.

In the application-centric approach, business logic lives in service classes that share mutable state, call databases mid-computation, and accumulate hidden dependencies. A "helper function" can do anything the programming language permits --- and often does. Reuse degrades because every helper carries invisible baggage: constructor parameters, initialization sequences, database connections, cached state. Three teams need the same computation. Each copies the code rather than risk the hidden dependencies. Object-oriented programming promised "write once, use everywhere." Implicit coupling made that promise structurally undeliverable.

In PGS, computation is governed. A CT_ atom is a pure function with a declared contract: these inputs in, those outputs out, nothing else touched. An atom that works in one context works in every context --- not because engineers are disciplined, but because the architecture prohibits the conditions that would make reuse fail.

## 6.2 --- The CT Atom

**Definition:** A CT atom is a single-purpose, side-effect-free transform that maps declared inputs to declared outputs.

**Key Properties:**

1.  **Deterministic.** Same inputs produce same outputs, every time, on every machine.
2.  **No external state access.** No database reads, no API calls, no file I/O, no ambient clock, no randomness unless explicitly injected.
3.  **Explicit input and output schema.** Every input and every output is declared in the governance artifact. The atom cannot consume undeclared inputs or produce undeclared outputs.
4.  **Versioned and immutable.** CT_PURE_GENERATE_ID_V0 is a structural fact --- it cannot be modified in place. Changes require a new version. Both versions coexist --- CT_PURE_GENERATE_ID_V0 and CT_PURE_GENERATE_ID_V1 can live side by side in the registry. Molecules and CC_ pipelines reference explicit versions. There is no "latest" --- there is only the version you declared.
5.  **Resolved via Runtime Binding.** Like CS_ side effects, CT_ atoms are not invoked directly. The engine resolves each CT_ code to its concrete implementation through an RB_ (Runtime Binding) artifact at startup. This keeps the runtime fully implementation-agnostic: it dispatches to `CT_PURE_GENERATE_ID_V0` as a protocol identifier, not as a class name or import path. The binding from identifier to implementation is declared, not discovered.

### Example 6.1 --- CT_PURE_GENERATE_ID_V0

*(The full artifact is provided in Appendix B, Example 6.1.)*

The implementation is a pure function:

    def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        prefix = inputs["prefix"]
        data = inputs["data"]
        id_value = generate_deterministic_id(prefix=prefix, data=data)
        return {"id": id_value}

**Analysis:**

- **The atom is a functional mapping.** Inputs go in. Outputs come out. Nothing else is touched. The function does not read from a database to check for collisions. It does not write to a log. It does not consult a cache. Its entire world is the `inputs` dictionary.
- **No ambient authority.** The atom cannot reach outside its declared inputs. There is no `self.db`, no injected service, no global variable. The function's parameters are its complete dependency surface.
- **The governance artifact is the contract.** It declares what the atom accepts (prefix, data) and what it produces (id). The implementation must honor this contract. The CT executor validates inputs against the declared schema before dispatch.
- **Reuse is immediate.** Any CC_ pipeline in any domain can reference CT_PURE_GENERATE_ID_V0. The user registration workflow uses it to generate user IDs. A financial workflow could use it to generate transaction IDs. A device provisioning workflow could use it to generate device IDs. Same atom, different prefix, different data --- same structural guarantee.

### Example 6.2 --- CT_PURE_ECDSA_SIGN_V0

A domain atom from the blockchain package --- structurally identical to the reusable atom above *(see Appendix B, Example 6.2)*.

**Analysis:**

- **Same pattern, different domain.** The CT executor dispatches CT_PURE_ECDSA_SIGN_V0 exactly as it dispatches CT_PURE_GENERATE_ID_V0 --- resolve inputs, invoke the atom, collect outputs. The executor does not know what ECDSA is. It does not know what a private key is. It resolves symbols and invokes functions.
- **Security through purity.** Private key bytes enter as an input. They are consumed by the computation. They do not appear in the outputs --- only the signature components (v, r, s) are returned. The atom cannot leak secrets because it cannot write to a log, call an API, or store data anywhere except its declared outputs. Purity is a security property, not just a correctness property.
- **Domain-specific computation, domain-agnostic execution.** The cryptographic knowledge lives in the atom implementation. The execution framework knows nothing about cryptography. This is the WHAT/HOW separation applied at the transform level.

## 6.3 --- The Molecule

**Definition:** A molecule is a deterministic composition of CT atoms into a single transform unit with explicit dataflow between steps.

**Key Properties:**

1.  **Ordered step execution.** Steps execute in declared sequence --- step 1, then step 2, then step 3.
2.  **Explicit dataflow.** Every step declares where its inputs come from: `$.inputs.field` for molecule inputs, `$.results.previous_step.field` for intermediate values. There is no implicit data passing.
3.  **No implicit control flow.** Molecules are linear pipelines. There is no branching, no conditionals, no loops. Conditional routing belongs in the workflow layer (WF_), not the transform layer. Loops are excluded deliberately: loops would make transform termination a runtime property. PGS requires termination to be structurally guaranteed --- deterministic at authoring time, not discovered at execution time.
4.  **Compositional closure.** A molecule is itself a CT --- it composes as an atom from the engine's perspective. Molecules can compose other molecules.

### Example 6.3 --- CT_PURE_MNEMONIC_TO_KEY_AND_ADDRESS_V0_MOLECULE

A molecule that derives a blockchain address from a mnemonic phrase --- composing four atoms with explicit dataflow *(see Appendix B, Example 6.3)*.

**Step Binding Expansion Rules:**

The shorthand bindings in the molecule expand to full symbol paths:

  -------------------------------------------------------------------------------------------------------------------------
  Shorthand                              Expands To                                       Meaning
  -------------------------------------- ------------------------------------------------ ---------------------------------
  `mnemonic`                             `$.inputs.mnemonic`                              Molecule input

  `generate_seed.seed_bytes`             `$.results.generate_seed.seed_bytes`             Previous step output

  `derive_key.value.private_key_bytes`   `$.results.derive_key.value.private_key_bytes`   Nested field from molecule step

  `path_indices`                         `$.inputs.path_indices`                          Molecule input
  -------------------------------------------------------------------------------------------------------------------------

**A note on** `.value` **semantics:** When a molecule invokes another molecule as a step (e.g., `CT_PURE_DERIVE_BIP32_PATH_V0_MOLECULE`), the inner molecule's result is wrapped in a `.value` envelope --- a canonical payload wrapper that unifies pipeline integration. The binding `derive_key.value.private_key_bytes` unwraps through this envelope to reach the actual computation result. This wrapping is not arbitrary nesting --- it is the standard CT result envelope that separates "the computation output" from "the protocol status." Chapter 7 develops this integration fully when CT results flow through the CC pipeline.

**Analysis:**

- **Composition is declared, not coded.** The molecule is a governance artifact. The dataflow is visible by reading the YAML --- no code inspection required. An auditor can trace every input from its source to its destination without opening a single Python file.
- **Intermediate values are named and traceable.** `generate_seed`, `derive_key`, `derive_pubkey`, `assemble_result` --- each step produces a named result. There are no anonymous temporaries, no implicit pipelines, no hidden intermediate state.
- **The molecule is pure because its atoms are pure.** If every step is side-effect-free, the composition is side-effect-free. Purity composes upward. This is not an assumption --- it is a structural guarantee enforced by the CT executor.
- **Reuse compounds.** The molecule itself is reusable as a single atom in larger compositions. `CT_PURE_DERIVE_BIP32_PATH_V0_MOLECULE` (step 2) is itself a molecule --- composed of lower-level atoms. Composition is recursive. The CT executor handles it uniformly.

## 6.4 --- CT-IR: The Intermediate Representation

**Definition:** CT-IR is the normalized internal representation that the CT executor consumes. Both atoms and molecules compile to CT-IR.

**Key Properties:**

1.  **Uniform format.** Every CT-IR has an `atom_stream` --- an ordered list of steps, each with `atom` (the code to invoke), `args` (symbol bindings), and `out` (the name to store the result under).
2.  **Symbol resolution.** `$.inputs.X` resolves to the CT's declared input. `$.results.step.field` resolves to a field from a previous step's output.
3.  **Pre-validated.** The CT-IR is constructed at build time, not at execution time. Invalid bindings (references to undefined steps) are caught during compilation.
4.  **Immutable at execution time.** The CT executor cannot modify the CT-IR it executes --- by construction, not by convention.

### Example 6.4 --- CT-IR: Atom vs. Molecule

**Atom CT-IR** (CT_PURE_GENERATE_ID_V0) *(see Appendix B, Example 6.4a)*.

**Molecule CT-IR** (CT_PURE_MNEMONIC_TO_KEY_AND_ADDRESS_V0_MOLECULE) *(see Appendix B, Example 6.4b)*.

**Analysis:**

- **The executor sees no difference.** Both formats have `atom_stream` and `outputs`. The atom has one step. The molecule has four. The CT executor iterates the stream, resolves symbols, invokes atoms, stores results. It does not know which is which --- and does not need to.
- **CT-IR is the WHAT/HOW separation within transforms.** The authoring syntax (governance YAML with shorthand bindings) is the WHAT --- what the molecule computes. The CT-IR is the HOW --- how the executor processes it. Authors write YAML. The builder compiles CT-IR. The executor runs CT-IR. Three concerns, three representations, zero entanglement.
- **Deterministic lowering.** The same governance YAML always produces the same CT-IR. The same CT-IR always produces the same execution. Determinism flows from authoring through compilation through execution --- unbroken.

> **[DIAGRAM 3] --- The CT Transform Pipeline**

    Governance YAML  →  Builder  →  CT-IR  →  CT Executor  →  Trace
    (Authoring)         (Compile)    (Lowered)   (Dispatch)     (Record)

> This mirrors the system-level pipeline from Chapter 4 (governance artifacts → builder → compiled protocol → execution engine → trace) --- applied at the computation level. The WHAT/HOW separation operates at every scale.

## 6.5 --- Validation and Failure Surface

The CT layer has its own failure surface --- distinct from governance validation (Chapter 3), compilation (Chapter 4), and runtime execution (Chapter 5).

### Transform Validation Checks

  -----------------------------------------------------------------------------------------------
  Step                    Check                      Failure Condition
  ----------------------- -------------------------- --------------------------------------------
  1                       Input schema validation    Required input missing or wrong type

  2                       Output schema validation   Atom returns undeclared output key

  3                       Purity enforcement         CT_PURE atom attempts external I/O

  4                       Step binding resolution    Molecule references undefined intermediate

  5                       Atom registry lookup       CT-IR references unregistered atom code
  -----------------------------------------------------------------------------------------------

### Broken Example: Molecule with Undefined Reference

A molecule step attempts to reference a step that does not exist *(see Appendix B, Example 6.5)*.

The CT-IR builder rejects this at build time:

    CT-IR CONSTRUCTION FAILURE
      Artifact:   CT_PURE_BROKEN_MOLECULE_V0
      Step:       derive_key
      Check:      Step binding resolution
      Binding:    seed_bytes: $.results.generate_seed.seed_bytes
      Detail:     Symbol "generate_seed" is not defined.
                  No prior step produces this output.
      Available:  [] (no prior steps)
      Resolution: Add a step that produces "generate_seed" before this step,
                  or bind to a molecule input ($.inputs.X)

### Broken Example: Atom Violating Purity

An atom implementation attempts to read a file:

    def execute(inputs: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        with open("/etc/config.json") as f:    # VIOLATION
            config = json.load(f)
        return {"result": compute(inputs, config)}

This atom is classified `ct_pure` in its governance artifact. The purity contract prohibits I/O. The violation is caught at validation:

    PURITY VIOLATION
      Atom:       CT_PURE_IMPURE_HELPER_V0
      Category:   CT_PURE
      Violation:  File I/O detected in pure transform
      Detail:     Pure transforms cannot perform file reads, writes,
                  network calls, or any external state access.
      Resolution: Move I/O to a CS_ capability side effect, or
                  pass the required data as a declared input.

**This section proves:** CT failures are structural and pre-runtime. Molecule binding errors are caught at build time. Purity violations are caught at validation. The distance between authoring a broken transform and discovering the failure is zero.

## 6.6 --- Structural Insight (Doctrine Moment)

The reader has seen atoms execute as pure functions, molecules compose atoms with explicit dataflow, and CT-IR normalize both into a uniform execution format. At no point did the CT executor interpret domain semantics. It resolved symbols. It invoked functions. It collected outputs.

This is Chapter 2's **Property 4 --- Compositional Isolation** made operational within the transform layer. Pure transforms compose without side-effect contamination because the architecture prohibits the conditions that would cause contamination. A CT_PURE atom cannot access external state --- not by convention, but by construction.

**Invariant I-T1 --- Pure Transform Determinism:** Identical inputs to a CT atom or molecule always produce identical outputs and identical execution traces. This invariant is constitutional. The architecture prohibits non-deterministic inputs (ambient clock, randomness) unless explicitly declared. It prohibits side effects (database access, file I/O) unconditionally for CT_PURE. Determinism is not a testing aspiration --- it is a structural guarantee.

**Structural impossibility:** The CT executor cannot skip steps in the atom_stream, reorder steps, inject computation not declared in the CT-IR, or allow a CT_PURE atom to perform I/O. The executor is a symbol resolver and function dispatcher --- it does not decide what to compute or how to compute it.

### The Reuse Invariant

An atom that works in one context works in every context. This is not a design aspiration --- it is a structural consequence of three architectural properties:

1.  **Purity** --- no hidden state, no implicit dependencies, no side effects
2.  **Declared interfaces** --- inputs and outputs are the atom's complete dependency surface
3.  **Domain-agnostic execution** --- the CT executor does not know what domain the atom serves

Object-oriented programming promised exactly this: write a class once, reuse it everywhere. The promise failed because objects carry implicit state (fields that must be initialized), inherit hidden behavior (superclass methods that change without notice), and depend on runtime context (dependency injection, singletons, environment configuration). Each hidden dependency is a coupling point. As the system grows, coupling accumulates. Reuse becomes risky. Teams copy code rather than risk the hidden dependencies. Duplication replaces composition.

Atoms have none of these failure modes. An atom's inputs are its complete world. Compose it into any molecule, reference it from any CC_ pipeline, use it in any domain. The atom does not know or care where it runs. As the system expands, the atom library expands with it --- and every atom is immediately available to every domain, every workflow, every capability contract. The reuse that OOP promised is now a structural reality.

**Invariant I-T2 --- CT/CS Separation:** Pure computation (CT_) and world mutation (CS_) must never co-exist in the same artifact. A CT_ atom cannot invoke a CS_ operation. A CS_ step cannot be embedded inside a molecule. Crossing the boundary requires a capability contract (CC_) --- the governing artifact that declares which CT_ and CS_ steps execute, in what order, with what permissions. This invariant is what makes Chapter 7 structurally necessary: the CT/CS boundary is not a convention to be followed but a constitutional law to be enforced.

### Why Not "Just Functional Programming"?

An advanced reader may observe: atoms are pure functions. Molecules are function composition. Is this not simply functional programming?

It is --- and it is more. Functional programming gives purity and composition. PGS adds what FP alone does not provide:

- **Governance versioning.** Every atom is a versioned, immutable governance artifact --- not a function in a module that changes on the next commit.
- **Constitutional validation.** Atom contracts are validated against constitutional schemas at authoring time --- not by type inference or unit tests.
- **Transform registry.** Atoms are registered in a federated discovery system. Any domain can reference any atom by code --- no import paths, no dependency management.
- **Structural isolation from side effects.** The CT/CS boundary is architectural, not conventional. Haskell's IO monad marks effects at the type level. PGS prevents them at the vocabulary level --- CT_ artifacts cannot contain CS_ operations by construction, not by discipline.
- **Engine semantic blindness.** The CT executor does not interpret what atoms compute. FP runtimes are general-purpose --- they execute whatever code the programmer writes. The CT executor is a governed dispatcher --- it executes only what the CT-IR declares.

Functional programming provides the right computational model. Protocol governance provides the right authority model. Atoms are both.

This is not a minor convenience. It is an economic inflection point. In application-centric systems, the cost of the Nth domain includes re-implementing computation that already exists elsewhere in the system --- because reusing it is riskier than rewriting it. In PGS, the cost of the Nth domain includes only the domain-specific atoms it needs. Every reusable atom it inherits from the existing library is free --- structurally free, not aspirationally free.

## 6.7 --- Solved Problems

### Problem 6.1 --- Hidden Side Effects in Business Logic

**Scenario:** A validation helper writes an audit log entry as a "side effect" of computing a validation result.

**Application-Centric Approach:** The function `validate_user(record)` checks field validity AND writes to the audit database. Callers assume it is pure --- it is not. Moving the function to a different context breaks the audit trail or causes duplicate writes. The function's actual dependency surface is invisible. Reuse is impossible without understanding every hidden side effect.

**PGS Approach:** 1. CT_ atoms cannot call CS_ operations --- the boundary is architectural, not conventional 2. Validation is CT_PURE: it takes inputs, produces outputs, touches nothing else 3. Audit logging is a separate CS_ step declared in the CC_ pipeline --- visible, governed, independently evolvable 4. The validation atom is reusable in any context because it has no hidden dependencies to satisfy

**Eliminated pathology:** Implicit mutation. Side effects cannot hide inside pure computation because the architecture does not permit CT_ to perform them.

### Problem 6.2 --- Non-Deterministic Helpers

**Scenario:** A computation helper calls `datetime.now()` to generate a timestamp or `random.random()` to generate entropy.

**Application-Centric Approach:** The function produces different results on each call. Tests require mocking the clock and the random source. Replay is impossible without reproducing exact runtime conditions. Debugging a production issue requires guessing what `now()` returned at the time of the incident.

**PGS Approach:** 1. CT_PURE atoms cannot access the ambient clock or randomness source 2. If a computation needs a timestamp, it is passed as a declared input --- visible, reproducible, auditable 3. If a computation needs entropy, the entropy is injected explicitly --- the atom's governance artifact declares it 4. Determinism is constitutional: same inputs always produce same outputs. Replay is trivial

**Eliminated pathology:** Non-reproducible computation. Every CT_ execution is deterministic and replayable by construction.

### Problem 6.3 --- Duplication Through Fear of Reuse

**Scenario:** Three teams in three domains need deterministic ID generation. Each writes their own implementation.

**Application-Centric Approach:** The existing `IdGenerator` class requires a database connection for collision checking, a configuration object for prefix rules, and an initialization call that sets up a cache. Team B's domain does not use the same database. Team C's prefix rules differ slightly. Rather than untangle the dependencies, both teams copy the core algorithm into their own services. Three implementations drift independently. A bug found in one must be fixed in all three --- if anyone remembers they exist.

**PGS Approach:** 1. CT_PURE_GENERATE_ID_V0 is a governed atom: declared inputs (prefix, data), declared outputs (id), no hidden dependencies 2. Any CC_ pipeline in any domain references it by code --- no constructor, no initialization, no database connection 3. One atom, one governance artifact, one implementation, one version 4. Team B passes a different prefix. Team C passes different data. Same atom. Same guarantee. Zero duplication

**Eliminated pathology:** Duplication through coupling fear. Atoms are reusable by construction --- their inputs are their complete dependency surface. As the system grows, the atom library grows with it. Every new domain inherits every existing atom. The reuse dividend compounds.

## 6.8 --- Generated Output: The CT Execution Trace

The CT executor produces a step-by-step trace of atom execution. This trace is the structural proof of what the transform computed.

### Trace: CT_PURE_MNEMONIC_TO_KEY_AND_ADDRESS_V0_MOLECULE

    CT_EXEC_START
      molecule: CT_PURE_MNEMONIC_TO_KEY_AND_ADDRESS_V0_MOLECULE
      inputs: {mnemonic: "abandon abandon ... about",
               passphrase: "",
               path_indices: [2147483692, 2147483708, 2147483648],
               curve: "secp256k1"}

      STEP 1: CT_PURE_MNEMONIC_TO_SEED_V0
        args: {mnemonic: $.inputs.mnemonic,
               passphrase: $.inputs.passphrase}
        out: generate_seed
        status: SUCCESS

      STEP 2: CT_PURE_DERIVE_BIP32_PATH_V0_MOLECULE
        args: {seed_bytes: $.results.generate_seed.seed_bytes,
               path_indices: $.inputs.path_indices}
        out: derive_key
        status: SUCCESS

      STEP 3: CT_PURE_PRIVATE_KEY_TO_PUBLIC_V0
        args: {private_key_bytes: $.results.derive_key.value.private_key_bytes,
               curve: $.inputs.curve}
        out: derive_pubkey
        status: SUCCESS

      STEP 4: CT_PURE_ASSEMBLE_RECORD_V0
        args: {public_key_uncompressed_bytes: $.results.derive_pubkey.public_key_uncompressed_bytes,
               eth_address_hex: $.results.derive_address.eth_address_hex}
        out: assemble_result
        status: SUCCESS

    CT_EXEC_END
      output_symbol: assemble_result
      total_steps: 4
      deterministic: true

**What the trace proves:**

- **Every atom execution is visible.** Four steps, four atoms, four results. No hidden computation exists outside the declared atom_stream. The trace is a faithful record of the CT-IR.
- **Dataflow is explicit.** Each step's `args` shows exactly where each input came from --- molecule inputs (`$.inputs`) or previous step outputs (`$.results`). An auditor can trace any value from its origin to its consumption without reading code.
- **The trace is replayable.** Provide the same inputs to the same molecule. The same atoms execute in the same order with the same bindings. The outputs are identical. This is not a test assertion --- it is a structural guarantee of I-T1.
- **The executor did not interpret meaning.** It did not know what a mnemonic is, what BIP32 derivation means, or why the curve is secp256k1. It resolved symbols, invoked atoms, stored results, and moved to the next step. Semantic blindness at the transform level mirrors semantic blindness at the execution level (Chapter 5).

**Structural impossibility:** The CT executor cannot skip steps, reorder steps, or inject computation not declared in the CT-IR. The trace is a faithful record of the atom_stream --- nothing more and nothing less. If the trace records four steps, the CT-IR declared four steps. There is no mechanism for the executor to deviate from the declared stream.

You authored governance artifacts for atoms and molecules. The builder compiled them to CT-IR. The CT executor ran the atom_stream. The trace recorded every step. At no point did the executor know what it was computing --- and that is the point.

## 6.9 --- Boundary and Forward Pointer

This chapter proved that pure computation can be governed structurally --- through atoms with declared interfaces, molecules with explicit dataflow, and CT-IR as a uniform execution format. It proved that atom purity enables structural reuse: atoms compose without coupling, scale without duplication, and execute without domain awareness.

**What this chapter did not cover:**

- World mutation (CS_) --- how governed side effects interact with databases, files, and external systems (Chapter 7)
- The CC pipeline's `.value` wrapping --- how CT results are wrapped as `{"value": <output>, "result_status": "SUCCESS"}` before integration into the capability contract result (Chapter 7)
- Persistence guarantees, retry semantics, and idempotency for I/O operations (Chapter 7)
- The full failure taxonomy across all layers (Chapter 8)

**What comes next:** Chapter 7 opens the CS_ layer --- Capability Side Effects --- where controlled world mutation occurs under constitutional constraint. The reader will see how the CT/CS boundary is the paradigm's most important governance invariant. On one side: pure computation that composes freely, reuses structurally, and replays deterministically. On the other: governed world interaction that writes databases, appends event logs, and registers state --- each operation declared, each mutation authorized, each side effect visible.

The CT/CS boundary is not organizational. It is constitutional.

## 6.10 --- Review Questions

1.  **True or False: A CT_PURE atom may read from a database if it does not write to it.**

- *False. CT_PURE atoms cannot perform any I/O --- reads or writes. All inputs must be passed through declared parameters. Database access is a side effect regardless of direction. If an atom needs data from a database, a prior CS_ step must retrieve it and pass it as an input.*

2.  **What structural guarantee does CT-IR provide?**

- *CT-IR normalizes both atoms and molecules into a uniform execution format (atom_stream with symbol resolution). The CT executor handles all transforms identically --- it does not distinguish atoms from molecules. Authoring syntax (governance YAML) is separated from execution structure (CT-IR JSON). This is the WHAT/HOW separation applied within the transform layer.*

3.  **Can a molecule branch conditionally? Why or why not?**

- *No. Molecules are linear pipelines --- ordered step sequences with explicit bindings. There is no* `if/else` *in the molecule grammar. Conditional routing belongs in the workflow layer (WF_), where edges declare outcome-based paths. This keeps the CT layer deterministic and compositionally pure.*

4.  **Why does atom purity enable structural reuse?**

- *A pure atom's inputs are its complete dependency surface. It has no hidden state, no initialization sequence, no runtime context requirements, no implicit dependencies. Any CC_ pipeline in any domain can reference it without understanding anything beyond its declared input/output schema. Reuse is a structural consequence of purity and declared interfaces --- not a design aspiration.*

5.  **Explain the symbol resolution paths in CT-IR.**

- `$.inputs.X` *resolves to the CT's declared input named X --- provided by the CC pipeline when it dispatches the transform.* `$.results.step.field` *resolves to a specific field from a previous step's output in the molecule's internal symbol table. The first reaches outside the CT (to the pipeline). The second reaches within the CT (to intermediate results). Both are mechanical dictionary lookups --- no interpretation, no evaluation.*

6.  **What distinguishes a CT-level failure from a runtime failure (Chapter 5)?**

- *CT-level failures are transform-internal: missing inputs, undefined symbol references, purity violations, unregistered atom codes. Runtime failures (Chapter 5) are environment-level: missing protocol artifacts, unbound capabilities, expression resolution failures in the execution context. CT failures occur inside the transform. Runtime failures occur in the execution loop that dispatches to the transform.*

7.  **How does the atom model differ from object-oriented reuse?**

- *Objects carry implicit state (fields), inherit hidden behavior (superclasses), and depend on runtime context (dependency injection, singletons). Each hidden dependency is a coupling point. As systems grow, coupling accumulates and reuse becomes risky --- teams copy code rather than risk the dependencies. Atoms have none of these failure modes. An atom's inputs are its complete world. Purity eliminates hidden state. Declared interfaces eliminate hidden dependencies. Domain-agnostic execution eliminates context requirements. The reuse that OOP promised is structurally delivered.*
