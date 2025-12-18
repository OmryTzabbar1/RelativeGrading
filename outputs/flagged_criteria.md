# Flagged Criteria for Manual Review

**Generated:** 2025-12-17
**Total Flagged:** 4

These criteria were extracted but could not be automatically categorized into the predefined categories. Please review and either:
1. Add them to an existing category in CATEGORIES.md
2. Create a new category
3. Mark as irrelevant (exclude from scoring)

---

## Uncategorized Criteria

| Criterion | Students | Count | Weight | Suggested Category |
|-----------|----------|-------|--------|-------------------|
| Multi-Agent Orchestration | 38971, 38973, 38985 | 3 | 0.083 | DevOps or CodeQuality |
| Dual Interface (Multiple Frontends) | 38981, 59378 | 2 | 0.056 | CodeQuality |
| Voice Input Support | 38980 | 1 | 0.028 | CodeQuality |
| File Upload Support | 59376 | 1 | 0.028 | CodeQuality |

---

## Analysis

### Multi-Agent Orchestration
Found in 3 student projects that implemented multi-agent AI systems:
- **38971**: Multi-agent architecture with multiple exercises
- **38973**: Reflex UI with Pydantic-AI multi-agent system
- **38985**: Agent orchestration focus

**Recommendation:** Add to **CodeQuality** as an advanced implementation pattern, or create new **Architecture** category.

### Dual Interface
Found in 2 projects that provide multiple frontend options:
- **38981**: Multiple UI implementations
- **59378**: Multiple frontend choices

**Recommendation:** Add to **CodeQuality** category under keywords like "dual interface", "multiple frontends", "alternative ui".

### Voice Input Support
Found in 1 project:
- **38980**: Voice input functionality

**Recommendation:** Add to **CodeQuality** as an accessibility/advanced feature.

### File Upload Support
Found in 1 project:
- **59376**: File upload capability with Chainlit

**Recommendation:** Add to **CodeQuality** as a feature enhancement.

---

## Suggested CATEGORIES.md Updates

Add these keywords to **CodeQuality** section:

```yaml
CodeQuality:
  keywords:
    # ... existing keywords ...
    - multi-agent
    - agent orchestration
    - dual interface
    - multiple frontends
    - voice input
    - speech input
    - file upload
    - file attachment
```

Or create a new **Features** category:

```yaml
Features:
  keywords:
    - multi-agent
    - agent orchestration
    - dual interface
    - voice input
    - file upload
    - export
    - import
  description: "Advanced feature implementations beyond basic requirements"
```

---

## How to Resolve

1. Edit `.claude/skills/evaluating-student-projects/CATEGORIES.md`
2. Add keywords under appropriate category
3. Re-run evaluation (optional - scores won't change significantly)

Or manually update `criteria_graph.json` to assign categories directly.

---

**Note:** These 4 uncategorized criteria contribute only 0.19 weight (1.3% of total). Categorizing them improves report organization but has minimal impact on final grades.
