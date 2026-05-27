---
name: andaman-context
description: Domain context for Andaman printing business — forms, delivery notes, AWOMS app
tags: [personal, context, andaman]
tier: personal
estimated_tokens: 400
---

# Andaman Context

## Business
Andaman is a printing business based in Thailand. The digital project is **AWOMS** (Andaman Work Order Management System) — a Next.js web app managing:
- Customer orders for print jobs
- Delivery notes generation (PDF)
- Job tracking and workflow

## Tech Stack
- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Database**: (check project CLAUDE.md)
- **Key feature**: Delivery notes API at `/api/delivery-notes`

## Key Paths
- App: `~/Documents/Andaman/AWOMS/awoms-app/`
- API: `src/app/api/delivery-notes/`

## Business Rules
- Print jobs tracked by job number
- Delivery notes must be PDF-exportable
- Customer-facing documents in Thai + English
- Operators work on Mac (Safari + Chrome)

## Conventions
- Thai language in UI labels where appropriate
- Follow existing Next.js App Router patterns
- Delivery note format must match physical forms

## Do NOT
- Change the delivery note format without confirming with user
- Alter database schema without migration plan
