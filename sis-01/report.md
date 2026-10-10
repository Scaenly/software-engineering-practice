# SIS #01 — Software Engineering Fundamentals, With an AI in the Loop

**Topic:** 1.1

> Preparation draft, generated with AI assistance on 2026-10-10. The outline, review decisions, final edits and reflection below are assistant-authored. No earlier student commit or push is claimed. The student must read the sources, write their own reflection, review the text and complete the repository workflow.

## 1. Scenario

**Question:** What must a customer receive beyond program code when a study room booking website is delivered professionally?

**Users:** Students reserve rooms, and a campus administrator manages availability and bookings.

**Problem:** Paper reservations make availability unclear. The customer needs a usable service and enough information to operate, check and maintain it after handover.

**Constraints:** First, two student developers have four weeks to deliver. Second, the website must run on an existing campus server without paid cloud services.

**Risk:** Two students could receive confirmed bookings for the same room and overlapping times.

**Assumptions:** The campus, customer, team size, schedule and hosting arrangement are fictional. Existing student accounts are assumed. Payments and mobile applications are outside scope.

## 2. Analysis

Professional delivery should leave the customer able to use, operate and maintain the booking service. Program files alone do not explain what was agreed, how to install the release or what happens when faults appear. For this scenario, the delivery checklist should include requirements and acceptance criteria, a versioned release, installation and configuration instructions, role-specific guides, test evidence, known limitations and a support handover.

The first engineering decision is to make booking conflicts a release condition. Requirements should define overlapping times, cancellation and administrator permissions. For two valid simultaneous requests for the same room and overlapping period, exactly one should be confirmed; the other should receive a conflict message. The conflict check and booking write should be atomic, meaning they occur as one indivisible operation. This avoids another reservation being inserted between checking availability and saving. The database's capabilities still need checking. Tests should cover simultaneous requests, partial overlaps, invalid times, cancellations and unauthorized changes. These are proposed tests, not results from an implemented system. Passing tests cannot establish that all defects are absent [1].

The second decision is to keep documentation short and tied to the delivered version. Two developers have four weeks, so maintaining a large manual would compete with implementation and testing. However, omitting guidance could make the customer dependent on them. Students need booking and cancellation instructions. Administrators need availability and issue-handling guidance. The server operator needs dependencies, configuration, update steps and known limitations. Store the guides alongside the release and rehearse installation on the intended server. This supports the existing-server constraint without adding paid hosting.

Recovery instructions should include a rehearsal with fictional booking data. NIST recommends testing recovery procedures [2]. Restoring a saved copy may lose later changes, so the customer must agree acceptable data loss and backup frequency. These values are unknown; they should not be invented. The guidance supports this recommendation without making NIST a legal requirement for the campus.

Finally, agree a fault-reporting route, a responsible maintainer and any support period before handover. Do not promise a month automatically. A customer representative should review the agreed acceptance cases and limitations before accepting delivery. Existing account integration and server compatibility remain assumptions requiring confirmation.

## 3. Review

The six critique points received separate decisions. Point 1 was accepted: the draft's textbook-style definition needed support. The author-linked chapter could not be read, so the final analysis removes that definition and presents the delivery package as a scenario recommendation. It does not claim that an inaccessible source was verified.

Point 2 was accepted. Verification row 1 uses ISTQB section 1.3, principle 1, page 17, to keep the testing limitation. Successful tests provide evidence about exercised cases, not guaranteed correctness. This distinction matters because one successful booking says little about simultaneous requests.

Point 3 was accepted. Change-log row 1 replaces a vague simultaneous-request test with an explicit outcome and an atomic conflict check and write. This addresses the stated double-booking risk. It remains a proposed engineering decision; no database implementation was inspected.

Point 4 was accepted. Verification row 2 qualifies the broad backup claim using NIST sections 3.4.1 and 3.5.1. Change-log row 2 requires a recovery rehearsal and identifies possible loss of later changes. The source is technical guidance rather than a legal obligation for this fictional campus.

Point 5 was qualified. Support remains necessary, but change-log row 3 removes an automatic month because availability and responsibilities were never agreed. Point 6 was accepted: deployment must be rehearsed on the intended server, with a customer representative agreeing acceptance.

These decisions, source checks and revisions were performed by the assistant. The student has not independently verified them, edited the result or written the reflection. No student-authored outline was committed and pushed before preparation. The staged records document AI preparation, not three student-sent exchanges. Structural checker success cannot establish that these workflow requirements were met.

## 4. Conclusion

The recommended delivery is a small, versioned package containing the working website, agreed rules, installation guidance, role-specific instructions, test evidence, recovery guidance and a support handover. Booking conflicts should be a release condition because two confirmations for the same room would undermine the customer's main purpose. Short documents and a deployment rehearsal fit the four-week deadline and existing campus server.

The main limitation is that the campus and delivery arrangements are fictional. No actual server, account integration or booking implementation has been checked. The recommendations therefore guide a future delivery rather than certify readiness. The customer and developers must agree acceptance, acceptable data loss and maintenance responsibility before using the service. The student must also independently review this AI-prepared report.

## 5. Reflection

This is an AI-authored reflection draft, not the student's personal account of learning or completed independent work. It must be replaced with a reflection written by the student before submission.

The preparation illustrates how AI can turn a broad delivery question into a concrete checklist. The most useful comparison is between a website that can make one reservation and a service that the customer can install, check and maintain. The critique also exposes two specific weaknesses: treating backups as guaranteed protection and proposing a support period without agreement.

The source notes show why evidence should change the answer. Testing results have limits, and recovery requires more than creating a saved copy. The final draft therefore adds an explicit concurrency outcome, a recovery rehearsal and an agreed support handover.

An independent reflection should explain which of these ideas the student accepted, what they changed personally and what remains unclear. It should identify sources the student actually read and distinguish their own decisions from assistance. None of those personal actions is claimed here.

## 6. References

- [1] International Software Testing Qualifications Board (ISTQB). (2024). Certified Tester Foundation Level Syllabus, version 4.0.1, 2024-09-15. Section 1.3, principle 1, printed page 17 (PDF page 17). https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf Accessed by the assistant 2026-10-10; student reading is not claimed.
- [2] Swanson, M., Bowen, P., Phillips, A. W., Gallup, D., and Lynes, D. (2010). Contingency Planning Guide for Federal Information Systems. NIST Special Publication 800-34 Rev. 1. Sections 3.4.1 and 3.5.1, printed pages 20 and 27-28 (PDF pages 34 and 41-42). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf Accessed by the assistant 2026-10-10; student reading is not claimed.

## 7. Appendix A — Initial outline

> This outline was prepared by the assistant before its drafting stage. It was not written independently by the student and was not committed or pushed before Prompt A.

1. Agree the booking rules and acceptance criteria before deciding whether the website is ready.
2. Provide short student instructions and a separate administrator guide so both roles can use the service.
3. Test overlapping bookings, simultaneous requests and permissions rather than only a successful reservation.
4. Deliver installation, configuration and recovery instructions for the existing campus server.
5. Agree who handles faults and future updates after the two developers finish the project.

## 8. Appendix B — AI exchanges

> AI preparation record: the assistant constructed and applied the exact A/B/C prompt templates internally during this preparation session, then saved the generated outputs below. These are not three student-sent chat exchanges. The scenario, outline, critique judgments and final edits are AI-assisted. No independent student decisions or historical conversation messages are invented. Replace this preparation record with complete actual student-run exchanges if completing the prescribed workflow.

### B1 — Draft (Prompt A)

- **Tool:** ChatGPT Work
- **Model:** not displayed
- **Date:** 2026-10-10
- **Purpose:** contextual draft during assistant preparation

**Prompt:**

~~~~text
Act as a software engineering tutor. Help me analyze topic 1.1 Professional software delivery: Explain what a customer needs beyond program code. Use AI to propose a delivery checklist, then justify the documents, tests and support your scenario needs. for a first-year-level university assignment.

My scenario is a fictional campus where students reserve study rooms and an administrator manages availability. Paper reservations make availability unclear. Two student developers have four weeks to deliver, and the website must run on an existing campus server without paid cloud services. The main risk is confirmed overlapping bookings for the same room. Existing student accounts are assumed; payments and mobile applications are outside scope. My initial ideas are 1. Agree the booking rules and acceptance criteria before deciding whether the website is ready.
2. Provide short student instructions and a separate administrator guide so both roles can use the service.
3. Test overlapping bookings, simultaneous requests and permissions rather than only a successful reservation.
4. Deliver installation, configuration and recovery instructions for the existing campus server.
5. Agree who handles faults and future updates after the two developers finish the project.. Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
~~~~

**Response:**

~~~~text
Professional delivery means handing over a usable service rather than only the program files. Software includes documentation and configuration data needed to use the programs. For this fictional campus, the customer must be able to operate the booking website, judge whether it meets agreed needs and arrange maintenance when the student developers leave.

A suitable delivery checklist contains agreed requirements, the working release, installation instructions, user guidance, test evidence and a support plan. Requirements should explain room availability, booking confirmation, cancellation and administrator permissions. They should also define overlapping times. Otherwise, developers and the customer may disagree about whether two reservations conflict. Requirements are especially important because the main risk is giving two students confirmed reservations for the same room and time.

The first engineering decision is to concentrate testing on booking conflicts. Tests should cover overlapping reservations, cancellations, invalid times and attempts to change another student's booking. The team should also try simultaneous requests for the same room. A successful demonstration of one reservation is useful, but it does not establish how the website behaves when several students book together. Passing tests cannot prove that software contains no defects. The customer should receive the test cases, observed results and any known failures rather than only a statement that testing was completed.

The second decision is to use short documents suitable for a two-person team with four weeks. Students need instructions for finding a room, booking it and cancelling. The administrator needs guidance for changing availability and dealing with reported problems. The person running the existing campus server needs installation steps, required software versions and configuration instructions. A large collection of documents would take time away from development, but missing instructions could leave the customer dependent on the original developers. Keeping the guides in the same repository as the release would make updates easier to track.

Support should also be agreed before handover. The developers could provide one month of support, explain how faults are reported and identify who maintains the service afterwards. Backups protect bookings from server failures. The delivery should include backup instructions and a procedure for restoring saved data. The team should explain how to return to the previous release if an update causes problems. These measures fit an existing server and avoid introducing paid cloud services.

The scenario details, existing accounts and suggested support period are assumptions rather than facts about a real campus. The actual server configuration and responsible maintenance person remain unknown. Claims about software including supporting materials and the limits of testing should be checked in authoritative sources. The final delivery package should be small enough to maintain, while still giving the customer evidence and practical instructions for operating the website.
~~~~

### B2 — Critique (Prompt B)

- **Tool:** ChatGPT Work
- **Model:** not displayed
- **Date:** 2026-10-10
- **Purpose:** critical review during assistant preparation

**Prompt:**

~~~~text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: 1.1 Professional software delivery: Explain what a customer needs beyond program code. Use AI to propose a delivery checklist, then justify the documents, tests and support your scenario needs.. Scenario: a fictional campus where students reserve study rooms and an administrator manages availability. Paper reservations make availability unclear. Two student developers have four weeks to deliver, and the website must run on an existing campus server without paid cloud services. The main risk is confirmed overlapping bookings for the same room. Existing student accounts are assumed; payments and mobile applications are outside scope. Draft: Professional delivery means handing over a usable service rather than only the program files. Software includes documentation and configuration data needed to use the programs. For this fictional campus, the customer must be able to operate the booking website, judge whether it meets agreed needs and arrange maintenance when the student developers leave.

A suitable delivery checklist contains agreed requirements, the working release, installation instructions, user guidance, test evidence and a support plan. Requirements should explain room availability, booking confirmation, cancellation and administrator permissions. They should also define overlapping times. Otherwise, developers and the customer may disagree about whether two reservations conflict. Requirements are especially important because the main risk is giving two students confirmed reservations for the same room and time.

The first engineering decision is to concentrate testing on booking conflicts. Tests should cover overlapping reservations, cancellations, invalid times and attempts to change another student's booking. The team should also try simultaneous requests for the same room. A successful demonstration of one reservation is useful, but it does not establish how the website behaves when several students book together. Passing tests cannot prove that software contains no defects. The customer should receive the test cases, observed results and any known failures rather than only a statement that testing was completed.

The second decision is to use short documents suitable for a two-person team with four weeks. Students need instructions for finding a room, booking it and cancelling. The administrator needs guidance for changing availability and dealing with reported problems. The person running the existing campus server needs installation steps, required software versions and configuration instructions. A large collection of documents would take time away from development, but missing instructions could leave the customer dependent on the original developers. Keeping the guides in the same repository as the release would make updates easier to track.

Support should also be agreed before handover. The developers could provide one month of support, explain how faults are reported and identify who maintains the service afterwards. Backups protect bookings from server failures. The delivery should include backup instructions and a procedure for restoring saved data. The team should explain how to return to the previous release if an update causes problems. These measures fit an existing server and avoid introducing paid cloud services.

The scenario details, existing accounts and suggested support period are assumptions rather than facts about a real campus. The actual server configuration and responsible maintenance person remain unknown. Claims about software including supporting materials and the limits of testing should be checked in authoritative sources. The final delivery package should be small enough to maintain, while still giving the customer evidence and practical instructions for operating the website..
~~~~

**Response:**

~~~~text
1. Supporting materials: The definition of software is stated as a fact without a reference. It matters because it supports the central answer to the question. Check a software engineering textbook's definition and record an exact locator. An alternative is a self-contained utility requiring almost no configuration, so the amount of supporting material varies with the product.

2. Test evidence: The statement that passing tests cannot prove the absence of defects is appropriate but needs verification. Check a recognized testing syllabus. A single successful reservation is a counterexample to treating a working demonstration as evidence about simultaneous bookings; it exercises a different situation.

3. Concurrent booking: Trying simultaneous requests is useful, but the draft does not say what must happen or how the implementation prevents conflicting confirmations. Agree an acceptance case where exactly one overlapping request is confirmed. Check the chosen database and booking implementation. A sequential availability check can pass ordinary tests yet allow two concurrent requests to succeed.

4. Backup overstatement: "Backups protect bookings from server failures" is too broad. A backup can be unavailable, incomplete or impossible to restore, and later bookings may not be included. Check the restore procedure using fictional data. A backup stored only on the failed disk is a counterexample. Clarify recovery limitations instead of implying guaranteed protection.

5. Support assumption: One month of support is a proposal, not a requirement supplied by the scenario. It matters because the team cannot promise work without agreement. Check the customer's expectations and the developers' availability. Alternatively, campus IT could own support from handover if that responsibility is explicitly accepted.

6. Scope and environment: The short-document approach fits the deadline, but actual server dependencies and acceptance responsibility remain unclear. Check the campus server and obtain agreement on who signs off delivery. A guide based on an untested operating system would not make deployment repeatable. Avoid inventing performance limits or assigning an administrator technical duties without confirmation.
~~~~

### B3 — Revision (Prompt C)

- **Tool:** ChatGPT Work
- **Model:** not displayed
- **Date:** 2026-10-10
- **Purpose:** revision using assistant decisions and assistant-verified evidence

**Prompt:**

~~~~text
Revise the draft using my review decisions and source notes below. Keep the answer relevant to my scenario and preserve uncertainty where evidence is limited.

My decisions: 1. Accept the need to support the software definition, but remove the textbook-style definition from the final analysis because the author-linked chapter could not be read. Present the delivery package as a recommendation for this scenario instead. 2. Accept the testing limitation and keep it with the verified ISTQB reference. 3. Accept the concurrency concern: specify exactly one confirmation for two valid overlapping requests, and propose an atomic conflict check and write; actual database capability still needs checking. 4. Accept the backup concern: replace guaranteed protection with a recovery rehearsal and an explicit data-loss limitation. 5. Qualify the one-month support proposal: keep a support handover plan but leave its duration and responsible person for agreement. 6. Accept the environment concern: test deployment on the intended server and have the customer agree an acceptance representative. These are assistant-generated review decisions, not independent student judgments. Verified evidence: [1] ISTQB (2024), Certified Tester Foundation Level Syllabus v4.0.1, section 1.3, principle 1, printed page 17 (PDF page 17): passing tests do not establish the absence of defects. https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf (accessed 2026-10-10). Decision: keep. [2] Swanson et al. (2010), NIST SP 800-34 Rev. 1, sections 3.4.1 and 3.5.1, printed pages 20 and 27-28 (PDF pages 34 and 41-42): backup and recovery planning should be accompanied by tests of the recovery procedures. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf (accessed 2026-10-10). Decision: qualify the broad backup claim. NIST is used as technical guidance, not as a legal requirement for this fictional campus. Sources were opened and read by the assistant; student verification remains outstanding. Draft: Professional delivery means handing over a usable service rather than only the program files. Software includes documentation and configuration data needed to use the programs. For this fictional campus, the customer must be able to operate the booking website, judge whether it meets agreed needs and arrange maintenance when the student developers leave.

A suitable delivery checklist contains agreed requirements, the working release, installation instructions, user guidance, test evidence and a support plan. Requirements should explain room availability, booking confirmation, cancellation and administrator permissions. They should also define overlapping times. Otherwise, developers and the customer may disagree about whether two reservations conflict. Requirements are especially important because the main risk is giving two students confirmed reservations for the same room and time.

The first engineering decision is to concentrate testing on booking conflicts. Tests should cover overlapping reservations, cancellations, invalid times and attempts to change another student's booking. The team should also try simultaneous requests for the same room. A successful demonstration of one reservation is useful, but it does not establish how the website behaves when several students book together. Passing tests cannot prove that software contains no defects. The customer should receive the test cases, observed results and any known failures rather than only a statement that testing was completed.

The second decision is to use short documents suitable for a two-person team with four weeks. Students need instructions for finding a room, booking it and cancelling. The administrator needs guidance for changing availability and dealing with reported problems. The person running the existing campus server needs installation steps, required software versions and configuration instructions. A large collection of documents would take time away from development, but missing instructions could leave the customer dependent on the original developers. Keeping the guides in the same repository as the release would make updates easier to track.

Support should also be agreed before handover. The developers could provide one month of support, explain how faults are reported and identify who maintains the service afterwards. Backups protect bookings from server failures. The delivery should include backup instructions and a procedure for restoring saved data. The team should explain how to return to the previous release if an update causes problems. These measures fit an existing server and avoid introducing paid cloud services.

The scenario details, existing accounts and suggested support period are assumptions rather than facts about a real campus. The actual server configuration and responsible maintenance person remain unknown. Claims about software including supporting materials and the limits of testing should be checked in authoritative sources. The final delivery package should be small enough to maintain, while still giving the customer evidence and practical instructions for operating the website..

Show what you changed and why. Use only the sources I supplied. Flag remaining gaps instead of inventing details.
~~~~

**Response:**

~~~~text
Revised explanation

For this fictional campus, professional delivery should provide a working booking service together with the information and evidence needed to operate and maintain it. The customer should receive agreed booking rules, a versioned release, installation and configuration instructions, short guides for each role, test results, known limitations and an agreed support handover. This is a proposed delivery package for this scenario, rather than a claim that every software product needs identical documents.

The requirements should define availability, confirmation, cancellation and administrator permissions. They should state how overlapping times are treated and who accepts the release. Existing student accounts are assumed, but their integration has not been confirmed. Payments and a mobile application remain outside scope because two developers have only four weeks.

Booking conflicts deserve particular attention. Two valid requests for the same room and overlapping times should not both receive confirmation. A proposed acceptance case is that exactly one is confirmed and the other receives a conflict message. The conflict check and booking write should be performed atomically: one indivisible operation, so another request cannot reserve the same period between those steps. The actual database and transaction behavior need inspection before claiming that the solution prevents double bookings. Tests should include simultaneous requests, partial overlaps, cancellation and unauthorized changes. Passing tests cannot prove that software contains no defects [1]. Results therefore provide evidence about the cases exercised, not a guarantee.

Documentation should remain short enough for the team to maintain. Students need booking and cancellation instructions; the administrator needs availability and issue-handling guidance. Whoever operates the existing campus server needs dependencies, configuration steps and update instructions. A deployment rehearsal on that server should expose missing instructions. Keeping these materials with a named release helps a future maintainer identify the version they describe. This approach balances maintainability against the four-week deadline without requiring paid hosting.

Recovery should be demonstrated rather than promised. NIST guidance combines backup and recovery planning with testing recovery procedures [2]. For this scenario, rehearse restoring fictional booking data and record the outcome. Explain what changes made after the saved copy could be lost. Using NIST here is an engineering choice, not a claim that its federal-system requirements legally bind this campus.

The support handover should name the agreed fault-reporting route, the responsible maintainer and any support period the parties actually accept. No fixed month is promised. Server compatibility, account integration, the maintainer and customer approval remain gaps requiring agreement. The delivery package is a recommendation, not evidence that a real website has been built or tested.

Changes and reasons

- Removed the unsupported textbook-style definition; the author-linked chapter was not readable in this session.
- Made the concurrency outcome explicit because double confirmation is the scenario's main risk.
- Kept the testing limitation with verified evidence [1].
- Replaced the broad backup claim with a recovery rehearsal and data-loss limitation, using [2].
- Replaced an assumed one-month commitment with support arrangements requiring agreement.
- Added deployment and acceptance checks while preserving uncertainty about the real environment.
~~~~

## 9. Appendix C — Evidence tables

> Both checks and all revisions below were performed by the assistant. The student has not yet independently checked the evidence or edited the report. The final version column refers to this prepared draft.

### Verification table

| AI claim | Source and locator | Evidence found | Decision |
| --- | --- | --- | --- |
| Passing tests cannot prove that software contains no defects. | ISTQB (2024), Certified Tester Foundation Level Syllabus v4.0.1, section 1.3, principle 1, page 17. https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf Accessed 2026-10-10 by the assistant. | Test success does not establish defect absence. | keep |
| Backups protect bookings from server failures. | Swanson et al. (2010), NIST SP 800-34 Rev. 1, sections 3.4.1 and 3.5.1, pages 20 and 27-28. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-34r1.pdf Accessed 2026-10-10 by the assistant. | Recovery planning and testing are needed; merely having a backup does not establish successful recovery. | qualify |

### Change log

| AI wording / suggestion | Your final version | Reason for change |
| --- | --- | --- |
| The team should also try simultaneous requests for the same room. | For two valid simultaneous requests for the same room and overlapping period, exactly one should be confirmed; the other should receive a conflict message. The conflict check and booking write should be atomic. | The main scenario risk is two conflicting confirmations. An observable acceptance outcome and indivisible check and write address that risk; database behavior remains to be checked. |
| Backups protect bookings from server failures. | Recovery instructions should include a rehearsal with fictional booking data. Restoring a saved copy may lose later changes. | NIST sections 3.4.1 and 3.5.1 support recovery planning and testing. The earlier wording overstated what a backup alone establishes. |
| The developers could provide one month of support. | Agree a fault-reporting route, a responsible maintainer and any support period before handover. Do not promise a month automatically. | The four-week development deadline does not establish post-delivery availability. Support commitments require agreement. |
