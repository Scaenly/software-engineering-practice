### Step 5: Fill in `AI_USAGE.md`

Update `week-04/AI_USAGE.md`:

```markdown
# AI Usage Declaration

## Tool & Model Details
- **Tool:** ChatGPT
- **Model Name & Version:** OpenAI GPT-4o (gpt-4o-2024-08-06)

## Prompts & Interactions
1. **Initial Setup:** Sent requirements, scenario, and approved user stories asking the AI to wait.
2. **Task 1 (Use Case):** Sent prompt unchanged. AI generated basic use cases; corrected multiplicities and stereotypes.
3. **Task 2 (Class):** Sent prompt unchanged. AI generated class structure with incorrect `1..*` multiplicities; corrected to `0..*` and added rule note.
4. **Task 3A (Sequence):** Sent prompt unchanged. AI generated sequence diagram missing early R1 validation; updated sequence logic.
5. **Critique:** Opened new chat and pasted revised `.puml` files to obtain independent critique.