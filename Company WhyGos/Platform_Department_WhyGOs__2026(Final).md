KARTEL AI, INC.

Platform Department

2026 WhyGO Goals

| Department | Platform Engineering |
| --- | --- |
| Department Head | Niels Hoffmann, CTO |
| Reports To | Luke Peterson, President |
| Fiscal Year | January 1, 2026 - December 31, 2026 |
| Last Updated | January 2026 |
| Status | REVISED - Pending Executive Review |

# Executive Summary

The Platform Department builds the technical infrastructure that enables Kartel to scale. Platform's role is to make all the pieces fit together—connecting the Client Portal, Production Management, Generative Platform (built by Fill), and Community systems into a unified ecosystem with consistent user experience, data organization, and access controls.

In 2026, the department will focus on three strategic priorities:

- Deploy Enterprise Platform: Build the unified platform that manages the full client lifecycle—from job requests and asset ingestion, through LoRA training outputs and generated media, to client feedback and final deliverables—with full integration to Fill's Generative Platform.

- Enterprise Security & Compliance Readiness: Implement technical controls that protect client data and meet enterprise security requirements. This may include SOC2 certification if required by whale clients, but the core focus is ensuring all data, training, and workflows are built with enterprise-grade protections.

- Unified Identity & Access Management: Deploy centralized authentication that enables the Talent Engine user journey—from Community member through Generative Platform access to Production Platform when qualified for pod work—with single sign-on across all Kartel systems.

These WhyGOs ladder directly to Company WhyGOs #1 (Product-Market Fit), #2 (Operational Excellence), #3 (Talent Engine), and #4 (Enterprise Platform). Success in the Platform Department unlocks Kartel's ability to serve enterprise clients at scale while building a sustainable talent pipeline.

# Company WhyGO Alignment

| Department WhyGO | Ladders To | Connection |
| --- | --- | --- |
| #1: Deploy Enterprise Platform | Company #4 (Enterprise Platform) | Primary |
| #2: Enterprise Security & Compliance | Company #1 (PMF) + #2 (Ops Excellence) | Enabler |
| #3: Unified Identity & Access | Company #3 (Talent Engine) + #4 (Platform) | Enabler |

# WhyGO #1: Deploy Enterprise Platform

WHY

Current operations rely on manual coordination across client engagements. To support 10+ concurrent clients without linear headcount growth, Kartel needs a unified platform that manages the full client lifecycle—from job requests and asset ingestion, through LoRA training outputs and generated media, to client feedback and final deliverables. The Enterprise Platform gives enterprise clients a professional interface for collaboration and approval workflows, while giving internal teams (Production and Generative) the tools to manage work efficiently. Platform's role is integration: connecting Fill's Generative Platform into the larger ecosystem with proper data organization, user access, and workflow connections.

GOAL

Deploy the Enterprise Platform (Client Portal + Production Management) to support 10+ concurrent client engagements, with full integration to Fill's Generative Platform.

OUTCOMES

| Outcome | Q1 | Q2 | Q3 | Q4 | Owner |
| --- | --- | --- | --- | --- | --- |
| Production Management in use (jobs, milestones, resources, handoffs) | MVP | v1.0 | Iterate | Iterate | Niels |
| Client Portal live (job requests, asset management, feedback, deliverables) | MVP | v1.0 | Iterate | Iterate | Niels |
| Generative Platform integration (LoRA outputs, media assets accessible) | Spec | MVP | v1.0 | Iterate | Niels |

Note on Production Management: The Production Platform is already in operation. "MVP Q1" means basic functionality in use with ongoing optimization and refinement throughout the year. Wayan's team depends on this for handoff discipline enforcement.

## Platform Architecture

| Component | Builds | Purpose |
| --- | --- | --- |
| Client Portal | Platform (Niels) | Enterprise client interface for job requests, data upload, asset delivery, feedback, user management |
| Production Management | Platform (Niels) | Internal platform for managing jobs, milestones, resources, expenses, handoff tracking |
| Generative Platform | Generative (Fill) | ComfyUI workflows, LoRA training, client data access, media generation |
| Integration Layer | Platform (Niels) | Connects all systems: user access, data organization, API connections, asset flow |

# WhyGO #2: Enterprise Security & Compliance Readiness

WHY

Enterprise clients require demonstrated security maturity before approving vendors. The specific compliance requirements vary by client—some may require SOC2, others may have different standards. What's non-negotiable is that client data must be protected, and all data, training, and workflows must be built with enterprise-grade protections. Platform owns the technical controls (access management, logging, encryption, infrastructure hardening) that form the foundation of security readiness.

GOAL

Implement technical controls that protect client data and meet enterprise security requirements, achieving compliance certifications (e.g., SOC2) as required by whale client deals.

OUTCOMES

| Outcome | Q1 | Q2 | Q3 | Q4 | Owner |
| --- | --- | --- | --- | --- | --- |
| Security controls implemented (access mgmt, logging, encryption, infrastructure) | Baseline | Core | Complete | Audit-ready | Niels |
| Client data isolation verified (air-gapped where required) | Assessed | Implemented | Verified | Documented | Niels |
| Compliance certification (SOC2 or equivalent, if required by clients) | TBD | TBD | TBD | TBD | Niels |

Note on Compliance Certification: The specific need for SOC2 has not been defined yet. Timeline will be set based on whale client requirements. If a deal requires SOC2 Type I by a specific date, Platform will prioritize accordingly.

# WhyGO #3: Unified Identity & Access Management

WHY

Kartel's platform ecosystem spans multiple systems—Enterprise Platform, Generative Platform, Community systems, and Kartel Labs. Today, each system manages users independently with fragmented authentication. This creates duplicated effort, inconsistent access control, and friction for both internal users and clients. Most critically, the Talent Engine depends on a seamless user journey: community members need to flow from Discord into the open parts of the Generative Platform, then into Production Platform when they qualify for pod work. Unified identity makes this journey possible.

GOAL

Deploy unified authentication and centralized user management across all Kartel platforms, enabling the Community → Generative → Production user journey with single sign-on for all users (internal, client, and community).

OUTCOMES

| Outcome | Q1 | Q2 | Q3 | Q4 | Owner |
| --- | --- | --- | --- | --- | --- |
| Centralized user management system live | Spec | MVP | v1.0 | Live | Niels |
| Identity providers supported (Google, Discord) | 1 | 2 | 2 | 2 | Niels |
| Platforms integrated with SSO (Enterprise, Generative, Community, Labs) | — | 1 | 2 | 4 | Niels |
| Discord → Generative Platform connection (credits/generation access) | MVP | v1.0 | Live | Optimized | Niels |
| Full user journey functional (Community → Generative → Production) | Spec | MVP | Live | Optimized | Niels |

## Talent Engine User Journey (Enabled by Identity)

| Stage | User Status | Platform Access | Enabled By |
| --- | --- | --- | --- |
| Tier 1-2 | Community Member / Engaged Learner | Discord + Community tools | Discord identity provider |
| Tier 3-4 | Skill Verified / Trial Contributor | + Open Generative Platform (credits, challenges) | SSO from Discord → Generative Platform |
| Tier 5 | Approved Kartel Talent | + Production Platform (client work) | SSO with elevated permissions |

# Addendum A: Cross-Departmental Dependencies

The Platform Department is the integration layer that connects all other departments. Success depends on tight coordination with Production, Generative, Community, and Sales.

## Dependencies ON Platform (What Others Need From Niels' Team)

| Department | Dependency | Platform Delivers | Timeline |
| --- | --- | --- | --- |
| Production (Wayan) | Handoff tracking, job management | Production Management MVP | Q1 (in use) |
| Production (Wayan) | Client job submission workflow | Client Portal MVP | Q1-Q2 |
| Generative (Fill) | Asset flow, data organization | Generative Platform integration | Q2-Q3 |
| Community (Daniel) | Discord → Generative Platform connection for credits/generation | Discord identity + Generative Platform access | Q1 (MVP) |
| Sales (Ben) | Security documentation for enterprise deals | Security controls + compliance docs | As needed |
| Executive | Enterprise-grade data protection | Client data isolation, encryption | Q2+ |

## Dependencies FROM Platform (What Niels' Team Needs From Others)

| Department | Dependency | Deliverable Needed | Success Criteria |
| --- | --- | --- | --- |
| Generative (Fill) | Generative Platform API specs | API documentation, integration requirements | Q1 for Q2 integration |
| Generative (Fill) | Kartel Labs integration testing | Testing access, feedback on SSO | Q3 |
| Production (Wayan) | Production Management feedback | Workflow requirements, adoption feedback | Ongoing |
| Community (Daniel) | Community user requirements | Discord auth needs, tier progression rules | Q1 |
| Sales (Ben) | Client security requirements | Compliance needs from whale deals | As deals progress |

# Addendum B: Strategic Context

## Platform's Role: The Integration Layer

Platform doesn't build everything—it makes everything work together. Fill builds the Generative Platform (ComfyUI workflows, LoRA training, media generation). Daniel builds community engagement. Wayan runs production operations. Platform's job is to connect these pieces into a unified system with:

- Consistent user experience across all systems

- Proper data organization and asset flow

- Unified identity and access control

- Enterprise-grade security and compliance

## The 70% Problem Connection

Kartel's value proposition is solving the 70% Problem: generic AI tools deliver ~70% accuracy, but enterprise requires 100% brand consistency. Platform infrastructure enables this by:

- Managing client data securely (air-gapped, no third-party API exposure)

- Connecting LoRA training outputs to production workflows

- Enabling the feedback loop from approved outputs back to training

- Tracking the full asset lifecycle from ingestion to delivery

# Addendum C: Implementation Guide

## Q1 Priorities

Q1 is the foundation quarter. Critical deliverables:

| # | Deliverable | WhyGO | Deadline |
| --- | --- | --- | --- |
| 1 | Production Management MVP in use (optimization ongoing) | #1 | In progress |
| 2 | Client Portal MVP live | #1 | End of Q1 |
| 3 | Generative Platform integration spec complete | #1 | End of Q1 |
| 4 | Security controls baseline assessment | #2 | End of Q1 |
| 5 | Unified Identity spec complete | #3 | End of Q1 |
| 6 | First identity provider live (Google or Discord) | #3 | End of Q1 |
| 7 | Discord → Generative Platform connection MVP (enables credits/generation) | #3 | End of Q1 |
| 8 | Community user requirements gathered from Daniel | #3 | End of Q1 |

## Individual WhyGO Cascade

Once these Department WhyGOs are confirmed, each team member should develop their Individual WhyGOs that ladder up to these goals. Suggested alignment:

| Team Member | Role | Primary WhyGO Alignment |
| --- | --- | --- |
| Matthias Thoemmes | Full Stack Developer | #1 (Client Portal) + #3 (Identity frontend) |
| Lukas Motiejunas | Full Stack Developer | #1 (Production Management) + #1 (Gen Platform integration) |
| Zac Bagley | Backend Engineer | #2 (Security controls) + #3 (Identity backend) |

## Progress Tracking

Use these indicators in weekly/monthly reviews:

| Indicator | Meaning | Action |
| --- | --- | --- |
| [+] | On pace (100% of target) | Continue current approach |
| [~] | Slightly off-pace (within 20%) | Identify blockers, adjust tactics |
| [-] | Off-pace (more than 20% behind) | Escalate to leadership, reallocate resources |

# Approval & Sign-Off

These Department WhyGOs have been reviewed and approved for implementation.

| Role | Name | Date | Approved |
| --- | --- | --- | --- |
| CEO | Kevin Reilly |  | [ ] |
| President | Luke Peterson |  | [ ] |
| CTO | Niels Hoffmann |  | [ ] |

— End of Document —
