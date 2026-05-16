KMDS operates within the security and governance boundary already established by the enterprise Git repository and associated IAM controls. Rather than creating a parallel knowledge store with independent authorization semantics, KMDS derives context, visibility, provenance, and auditability directly from the repositories, branches, commit history, and organizational access policies it operates against. This allows architectural knowledge, operational context, and engineering decisions to remain cryptographically attributable to source-controlled artifacts while preserving existing enterprise compliance workflows. KMDS is therefore positioned as a context-aware augmentation layer for software and infrastructure repositories, not as a standalone data platform requiring separate trust assumptions. The system is designed to support enterprise-scale software delivery environments where security posture, provenance, and operational traceability are first-class concerns.



The conceptual workflow for KMDS is:

1. Clone remote repository, move to your required branch
2. Launch your python tool to work within the repository. If kmds is not installed, install KMDS within your python environment.
3. Use kmds or kmds-data-helper to generate documentation for your repository.
4. Review your work and kmds production wtih kmds-ui, save the KB to known location within your repo, say a kmds directory
5. Check in repo


Note that in the enterprise setting, the tool is used within a git repository. It works within the context of and inherits the security context of the repository in which it is working.
