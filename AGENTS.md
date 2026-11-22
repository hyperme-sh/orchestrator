# Hypermesh orchestrator contributor guidance

Read README.md and docs/release-policy.md. Retain both this file and release
policy in public distributions. Keep private business and operator material in
the private documentation repository.

## Ownership and runtime boundaries

Orchestrator owns host-market pricing and timing. AIuditor owns audit, safety and
RBAC; conductor owns model routing and cost. Preserve the shared renter/native
execution path, environment-only API key, per-run idempotency and lease cleanup.
Use owner HTTP contracts; do not perform payments or grant accounting balances.
Funding is not a usable host ticket. Keep legacy wire inputs compatible.

## Validation and CI

Run `bash scripts/check-package.sh` for unit/contract checks against source,
installed wheel and rebuilt source archive. Tests use mocked HTTP. Integration,
e2e and shared-resource runs belong in CI and the nightly batch; never start or
repeat those suites manually. Green PR CI and clean review complete issues;
nightly failures become new issues, not completion gates.

Jobs use GitHub-hosted `ubuntu-24.04`. Public PRs must not reach
private runners or receive publication credentials. PR validation is read-only.
Only validated merged-main container builds may update the GHCR TEST channel.
No artifact uploads, package bundles or test-release tags. Keep credentials out
of builds and expose the registry token only to the publication step.

## Version and publication authority

Keep the declared package version unchanged without explicit authorization.
Manual tags/releases and production promotion need authorization for the specific
target and action. Preserve historical tags and releases. TEST services follow
moving channels, with patch-compatible peer contracts and no deployment pins.
Image identity and source revision may be recorded for diagnostics.

Never add required reviewers, branch protections, approval rulesets, environment
approvals, CODEOWNERS approval requirements or human release/deployment gates
unless explicitly requested. Automated checks and advisory reviews are welcome.

## Scope and new resources (required)

### Stay in your repo
- Only change files in this repository. Don't edit another repo's code, workflows, deploy config, Terraform or registry references, even to unblock your own run.
- When a failure comes from another repo or service (a broken dependency, image, workflow, setting or API), open an issue in the owning repo, or comment on an existing one, with the failing run link and the error. Link it from your PR or issue, then stop work on that path and wait. Don't build a workaround, a copy, or a parallel path around it.
- Don't help another service's failing run unless an issue in that service's repo assigns the work to this repo.

### Design note before new resources
- Before adding any new Azure or cloud resource type, new service, new repository, new registry, Key Vault, database server, workspace or environment, or a second copy of anything that already exists, open a design note issue that says what it is, why the existing one can't be used, and its cost. Wait until Chris approves it in that issue.
- The PR that implements it must link the approved design note. PRs that add such resources without one will be closed.
- All cloud resources are declared in Terraform in FyberLabs/infra. Never create, change or delete cloud resources by hand (CLI, portal, SDK or scripts).
