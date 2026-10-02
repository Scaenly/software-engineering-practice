# AI Usage Disclosure

## Policy Compliance
This lab was completed under **AI Policy Level D**. AI was used as an active assistant to generate initial user stories, acceptance criteria, and PlantUML diagrams, followed by mandatory human review, correction, and verification.

## Tool and Model Details
* **AI Tool**: Google Gemini[cite: 4]
* **Exact Model Name**: Gemini 2.5 Pro[cite: 4]

## Summary of AI Contributions
1. **User Stories Generation**: Generated raw user stories using Prompt 1 from README Section 3[cite: 1, 2].
2. **Acceptance Criteria**: Generated Given/When/Then acceptance criteria using Prompt 2.
3. **PlantUML Diagram**: Generated initial PlantUML code for use case diagrams using Prompt 3.

## Human Review & Adjustments
* Reviewed all generated user stories to remove out-of-scope features (such as QR-code check-ins) and assign strict IDs (`US-01` to `US-08`)[cite: 1, 2, 4].
* Verified boundary conditions for booking rules R2 ($\le 2$ hours) and R3 (non-overlapping back-to-back bookings)[cite: 1].
* Corrected actor associations in PlantUML code to ensure `Send Confirmation` is triggered via `<<include>>` relationship rather than direct actor interactions[cite: 2, 4].