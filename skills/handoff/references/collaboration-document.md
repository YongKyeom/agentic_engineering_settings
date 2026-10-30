# Collaboration document reference

This compact fictional example demonstrates the requested hierarchy: opening summary, item overview, scope and priorities, decisions, related documents, then matching details with an explanatory diagram. Its content is not project evidence, source-code descriptions, or implementation requirements. Adapt the structure using actual project facts; choose real document depth from the task, not this sample.

---

# Request review proposal — fictional example

- Audience: service owner and developers
- Document state: draft

## 개요

Users cannot see a request's progress in this fictional scenario. Propose showing its status and agreeing when reviewers should act.

## 항목 한눈에

| # | Item | Why it matters | Proposal | Detail |
|---|---|---|---|---|
| 1 | Status display | Users need to know the next action | Show status beside the request summary | [Status](#collab-status) |
| 2 | Review timing | Reviewer expectations are unclear | Agree the timing with the service owner | [Timing](#collab-timing) |

## 작업 규모와 우선순위

| Order | Item | Scope | Reason |
|---|---|---|---|
| 1 | Status meaning | Wording and display, in this example | Meaning must be clear before choosing labels |
| 2 | Review timing | To be assessed | Depends on the owner's decision |

## 결정·확인이 필요한 사항

What does each status mean, and when should a reviewer act? Both need agreement; owners and dates are undecided.

## 관련 문서

No supporting documents are included in this fictional example.

<a id="collab-status"></a>

## 1. Status display

Show the status alongside the request summary so users can identify the next action. The diagram illustrates information placement, not a software architecture.

```text
Request summary
  +-- Current status
  +-- Next action
```

Review criterion: a user can explain the current state and next action from the summary.

<a id="collab-timing"></a>

## 2. Review timing

Agree the review timing before displaying a deadline. The service owner confirms the rule; developers then reflect the agreed wording. No deadline is set in this example.

## 협의 후 조치

Record the agreed status meanings and timing, then check whether the displayed guidance matches them.
