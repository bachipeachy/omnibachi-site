---
title: Chapter 13 — Building a Protocol-Governed Domain
date: '2026-04-23'
draft: false
weight: 15
slug: chapter-13-building-a-protocol-governed-domain
---

Chapters 3 through 12 taught us about the different parts of a special system. We learned how it makes sure things are done correctly, how it runs programs, how it handles changes, and how it keeps track of everything. Each chapter showed us one important rule or feature. But knowing what each part does is not the same as knowing how to build the whole system from the very beginning.

This chapter changes our focus from *how the system works* to *how to build it*. It answers a big question: **If you start with nothing but an idea for a new system, what are the exact steps to create a working system that follows all the rules, keeps good records, and can be checked for correctness?**

The answer isn't just a simple list of things to do. It's a set of eight important steps, or "acts," that must be done in a specific order. It starts with Act 0 (planning), followed by seven building steps: Structure, Govern, Validate, Compile, Bind, Execute, and Check & Fix. Each step has a "gate" -- a condition that *must* be met before you can move to the next step. The system itself makes sure these gates are followed. If you try to skip a step, the system will stop you. This chapter will show you how to build a small, complete system, explain common mistakes, and give you a guide for how the system understands and uses your rules. By the end, you'll have a clear, step-by-step way to build your own system.

## 13.1 --- The Goal of Our Building Project

Chapters 3 through 12 laid out a full plan for how our special system works. You've learned about how we manage words and terms, how we turn rules into working parts, how we run tasks, how we change things safely, how we watch for problems, how we keep things secure, and how we connect different parts. Each chapter proved one important rule. Together, these rules make sure our system is predictable, easy to check, and can be put together with other parts.

But knowing what each part does is not the same as knowing how to build a complete system.

Think about building a regular app. A developer might start by writing some code, testing it a little, and then adding rules later if problems pop up. The order of these steps can be messy. There's no guarantee that the final app is complete or correct.

This chapter will show you that building our special system isn't messy -- it *must* follow a fixed order because each step depends on the one before it.

**Your Job:** Build a new system that follows all our rules, starting from an empty folder. You need to get it to a point where it can run tasks, keep records, and be checked for correctness -- using only the rules we learned in Chapters 3--12.

**The Main Rule:** You can't just start with code. The rules (governance) must come *before* the code. The "builder" (a tool that checks your rules) must approve everything before you can even try to run anything. There are no shortcuts.

In the regular app world, a developer might write a piece of code, test it, add checks later, and write down how it works only when someone asks. Each of these steps can be skipped or done in any order. What "finished" means can be different for everyone.

In our special system, each building step has a "gate" -- a condition that *must* be met before the next step can begin. These gates aren't just suggestions. The system's tools (the builder, the rule-loader, and the engine) make sure you follow them. If you skip a step, the system will reject your work. So, the way we build isn't just a good idea. It's the *only* way to create a system that follows all the rules.

## 13.2 --- The Plan and the Seven Building Steps

Building our special system is like following a recipe with eight main steps. The first step is planning (we call this Act 0), and the next seven are for building. Each step builds on the one before it.

You can think of the process like this:

`planning → making a space → writing the rules → checking the rules → getting ready to run → connecting to code → running the system → final checks`

You must follow these steps in order. You can't check the rules before you've written them. You can't run the system before it's ready. The system itself will stop you if you try to skip ahead.

### Act 0 --- Making the Plan (The Specification)

**What you do:** Before you build anything, you need a very detailed plan. We call this "the specification." If you're starting a new project, you'll create this plan from scratch. If you're working on an existing project, you'll check and improve the plan.

**What this really means:** This step needs two things to start and creates one important thing at the end.

**First, you need to know what the business wants.** This is usually a simple document that explains the problem you need to solve. It's written in plain English, not technical terms. For example, a business might want a system to check if an AI assistant is allowed to perform a certain action based on a customer's subscription. The document would describe this problem, not the technical solution.

**Second, you need to know how our special system works.** You (the architect or lead builder) need to understand all the parts, like "capability contracts" and "workflows," so you can turn the business's problem into a smart design.

**The result is "The Plan" document.** This is the most important document you will create. It's a complete blueprint for your new system. It describes:

- The main task the system will do (the workflow).
- All the special checks it needs to perform (the capability contracts).
- Who or what will be using the system (the actors).
- All the important things that can happen (the events).
- All the new tools or functions you'll need to create.
- Where information will be stored.
- Exactly what should happen when a request is denied.
- All the tests you'll need to run to make sure everything works.

This plan is your single source of truth. When we built a real system for AI assistants, we looked at this plan during every single building step. It answered all our questions, like "What checks does this task need?" or "What happens when a request is denied?" Without a good plan, you have to make up answers as you go, which leads to mistakes and confusion.

**The Gate:** The plan must be reviewed and approved. It has to be complete. Every possible path, including when things go wrong, must be clearly laid out.

**The Main Rule for This Step:** Your plan must be complete enough for someone to build the entire system without having to guess or invent new rules along the way. If the builder has to stop and design something, the plan isn't finished.

**What this step is NOT:**

- It's not just a simple "to-do" list.
- It's not a database plan. Our system doesn't have a traditional database.
- It's not an API design. The plan itself describes the API.
- **It is not one of the official rule files.** The plan is a guide to help you write the official rules later. If you change an official rule file, you should update the plan to match, but the official rule file is what the system actually uses.

**How to Fix Mistakes:** If the plan is missing something, fix it now before you start building. Fixing the plan takes a few minutes. Finding a mistake in the plan when you're already trying to run the system can take hours or days to fix because you have to go back, change the rules, and rebuild everything.

**Think of it this way:** * **Step 0 is the creative part.** This is where you do all the hard thinking and designing. It requires knowledge and experience. * **Steps 1 through 7 are the building part.** This part is mechanical. You just follow the plan. The system's tools will check your work. If you find yourself having to design something in these steps, it means your plan from Step 0 was incomplete.

This separation is on purpose. We handle all the tricky design choices in one single step (Act 0), so the rest of the building process can be smooth, predictable, and checked by our tools.

### Act I --- Make a Space for Your System

**What you do:** You officially create a "space" for your new system. This tells the main builder tool where to find your new rules and how your system fits in with everything else.

**What this really means:** You'll edit a special file called the "FQDN tree." Think of this file as the master map of the entire project. You add a new entry to this map for your system (which we call a "package"). This entry says: * What your system's name is. * That it's a business-focused system (a `domain_pack`). * What other parts of the main system it's allowed to use (like shared tools).

By adding your system to this map, you make it visible to the builder tool.

**The Gate:** The builder tool can see and recognize your new system. If your system isn't on the map, the builder will completely ignore it, no matter how many files you've created.

**The Main Rule for This Step:** Every part of the system must be listed on the master map (the FQDN tree).

**How to Fix Mistakes:** If the builder can't find your system, the first thing you should check is the master map. Make sure your entry is correct. No amount of coding can fix a system that the builder can't see.

### Act II --- Write Down the Rules

**Action:** Now you write down all the official rules for your system. This includes defining the actors, events, workflows, and capability contracts. But here's the important part: you only *declare* the rules. You don't write the actual code that does the work yet.

**What this really means:** You create a set of plain text files (with a `.md` extension). Inside each file, you'll have a special section that describes the artifact's properties, like its name, what it does, and how it connects to other parts. Think of this as filling out official forms, not writing a program.

**The Gate:** You have a complete set of rule files. Every task (workflow) has a clear start and end. Every check (capability contract) knows what "success" or "failure" means. Every possible outcome, especially when something is denied, is clearly defined.

**The Main Rule for This Step:** All the words and terms you use must come from an approved list (the "vocabulary"). You can't give a part of your system a power that hasn't been officially declared.

**Rules to Follow:** * **Do NOT write the code for your tools (CTs) yet.** Rules always come before the code that does the work. * Every time something is denied or fails, it must lead to a clear "EXIT" point. The system is not allowed to fail silently. * Every piece of data you plan to use must have a clear path. You can't try to use data that doesn't exist.

**How to Fix Mistakes:** If the system complains about your rule files, you need to fix the rule files themselves. For example, if you used a term that isn't in the official vocabulary, you must correct it. You never fix these kinds of problems by changing the main system engine.

**Example:** Imagine a workflow that needs to check something. Your rule file would say that if the check is "SUCCESS," it should continue to the next step. If the check is a "VIOLATION," it should go to an "EXIT" step. This makes sure you've thought about both the happy path and the failure path. At this stage, you haven't written the code that *does* the check, you've only written the rule about what to do *after* the check is done.

### Act III --- Check Your Rules Against the Main Rulebook

**What you do:** You run a special tool that checks all the rule files you just wrote. This tool acts like a spell-checker and grammar-checker, but for your system's rules.

**What this really means:** The builder tool reads your new rule files and makes sure they follow the system's main "constitution." It checks if you used the right words from the official vocabulary and if you filled out all the required fields correctly.

**The Gate:** All of your rule files pass the check with no errors.

**The Main Rule for This Step:** You can't use powers or terms that haven't been officially declared in the system's constitution.

**How to Fix Mistakes:** If the checker finds a mistake, it will give you a very specific error message. For example, it might say `ERROR: Unknown result_status 'TIMEOUT'`. This tells you exactly what's wrong. You must fix the mistake in your rule file, not by changing the checker tool.

### Act IV --- Turn Your Rules into Working Parts

**What you do:** You run the main builder tool. This tool takes all your approved rule files and turns them into a format the system can actually understand and run. It's like compiling code, but for your rules.

**What this really means:** The builder tool does a few things in order: it discovers your new files, validates them (like in Act III), and then "materializes" them by creating new, clean, machine-readable versions in a special `protocol/artifacts/` folder. It also creates a `build_manifest.json` file, which is a receipt of everything it just built.

**The Gate:** The builder successfully creates all the working parts, the manifest receipt, and the snapshot passes admission control.

**Checks at this gate:** * **Matching Names:** The name of your rule file must match the name you wrote inside the file. * **Complete Rules:** Every rule must be complete and follow the system's template. * **Valid Connections:** If one rule mentions another, the builder checks to make sure that the other rule actually exists. * **FQDN 100% compliance:** Every artifact reference must use the full `domain::ARTIFACT_CODE_Vn` form. Short names cause a hard failure at the GOVERN stage --- there are no warnings. * **Conformance assertions:** Two hard assertions run during the GOVERN stage: `ASSERT_CC_STORAGE_OP_CONFORMANCE_V0` (checks every storage operation declared in a CC_ is properly bounded) and `ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0` (checks every runtime binding follows policy). Both fail the build if violated. * **Snapshot admission:** After materialization, the builder runs `assert_snapshot_valid()`. This gate verifies the snapshot is structurally complete before the runtime is permitted to load it. If this check fails, the snapshot is never attested and the runtime will refuse to start.

**The Main Rule for This Step:** The builder only builds what's in your official rule files. It doesn't just grab any file it finds on your computer.

**How to Fix Mistakes:** If the build fails, it means there's a mistake in your rule files. The error message from the GOVERN stage will identify the exact assertion that failed and which artifact caused it. Go back to your rule files (Act II) and fix the problem. If `assert_snapshot_valid()` fails, re-run the full build --- do not attempt to patch the snapshot by hand.

### Act V --- Connect Your Rules to Real Code

**What you do:** Now you connect your rules to the actual code that will do the work. This step makes sure that every rule you've written is linked to a real, working piece of code --- for both capability transforms (CT_) and capability side effects (CS_).

**What this really means:** Your rules will often need to do things like check data or save information. The code for these actions lives in the governed capability substrate (`pgs_capabilities`). In this step, you author an RB_ (Runtime Binding) artifact that maps every CT_ and CS_ code your domain uses to its concrete implementation and configuration. The same binding mechanism applies symmetrically to both: the system checks that every capability your rules reference has an entry in an RB_ artifact before any workflow executes.

**What to declare in your RB_ artifact:** - For each **CT_** code: the module path to the pure function implementation - For each **CS_** code: the runtime host class (e.g., `RegistryRuntime`, `AppendOnlyJsonlRuntime`) and its storage policy (file path, connection config, etc.)

**The Gate:** Every CT_ and CS_ capability used by your domain's workflows resolves through an RB_ binding. The chain from protocol declaration to concrete implementation is complete. The compiler enforces this in the GOVERN stage (S4) via `ASSERT_RB_BINDING_POLICY_CONFORMANCE_V0` --- a missing or policy-violating binding is a compile failure, not a runtime failure.

**Rules to Follow:** * New CT atoms you create should be simple, pure, and reusable. They shouldn't embed domain-specific business logic that would limit reuse. * CS_ runtimes must use one of the pre-approved host classes. Extending the host class registry requires a change to the runtime engine, not an RB_ artifact. * **Crucially, any new CT or CS implementation must be tested in isolation first.** This is much faster than debugging inside the full execution engine.

**How to Fix Mistakes:** If a capability is unresolved at startup, the engine halts before any workflow executes and reports the missing binding code. Go back to your RB_ artifact and add the missing entry.

### Act VI --- Run the System with Test Data

**What you do:** It's finally time to run your system! You'll create test data (we call it a "payload") to try out every possible path your workflow can take. It's very important to test not just the "happy path" where everything works, but also all the paths where things are expected to fail.

**What this really means:** You run a command to start your workflow, giving it your test payload. The system will execute the steps you defined in your rules.

**The Gate:** Every test run finishes and produces a "trace" --- a detailed, step-by-step record of everything that happened.

**Rules to Follow:** * Your test data must match what your rules expect to see. * **Don't just test the happy path.** A system that only works when everything is perfect is an untested system. Make sure you test what happens when a request is denied or a check fails.

**Your Best Friend, the Trace Examiner:** When something goes wrong, a special tool called the Trace Examiner will tell you exactly what failed, where it failed, and why. It gives you a clear hint on how to fix it. There are no "unknown errors."

**How to Fix Mistakes:** Read the error report from the Trace Examiner. It will point you to the exact rule file and line that needs fixing. You'll go back to your rule files (Act II), fix the mistake, rebuild (Act IV), and then run the test again (Act VI).

### Act VII --- Check the Records and Lock It Down

**What you do:** This is the final step. You carefully check the detailed records ("traces") from your test runs to make sure everything happened exactly as you planned.

**What this really means:** You confirm that the system is stable and predictable. We call this "locking it down."

**The Gate:** The system is officially "locked." This means running the same test with the same rules will always produce the exact same result and the exact same record, every single time.

**The Main Rule for This Step:** You must be able to perfectly repeat any event that happens in the system.

**The Final Proof:** Run the same test twice. If the records (traces) are identical, your system is stable. If they are different, it means something changed, and the Trace Examiner will help you find out what.
