The conceptual workflow for KMDS is:

1. Clone remote repository, move to your required branch
2. Launch your python tool to work within the repository. If kmds is not installed, install KMDS within your python environment.
3. Use kmds or kmds-data-helper to generate documentation for your repository.
4. Review your work and kmds production wtih kmds-ui, save the KB to known location within your repo, say a kmds directory
5. Check in repo


Note that in the enterprise setting, the tool is used within a git repository. It works within the context of and inherits the security context of the repository in which it is working.
