# Short description and review of CIS GitLab Benchmark v1.0.1 - 04-19-2024


## 1.1 Code Changes

### 1.1.1 Ensure any changes to code are tracked in a version control platform (Manual)

Use GitLab Runner and metrics to monitor deployed application for not commited code.
Tools like [hofund](https://github.com/logchange/hofund) or  expose metrics (f.e for prometheus) with git information about
dirtiness of repository.

Example:
```
hofund_git_info{branch="master",build_host="DESKTOP-AAAAA",build_time="2023-02-19T11:22:34+0100",commit_id="0d32d0f",dirty="true",} 1.0
```

Based on this metric, you can create alerts informing that some application is running with changes that has not been authorized.

### 1.1.2 Ensure any change to code can be traced back to its associated task (Manual)

Create [merge request templates](https://docs.gitlab.com/ee/user/project/description_templates.html) which will introduce
controls (f.e. in form of checkboxes) to verify all important elements where meet. One of 
this elements can be `[ ] issue is connected to this MR`. 

See also [merge request commit templates](https://docs.gitlab.com/ee/user/project/merge_requests/commit_templates.html) as 
interesting feature to implement this control and create company-wide standard for commit messages.

Next element, that implements this control is [commit message template for push rules](https://docs.gitlab.com/ee/user/project/repository/push_rules.html#validate-commit-messages) which 
requires from commit author to meet rules (f.e commit message must contain expression like `issue#1234`)

Using tools like [logchange](https://github.com/logchange/logchange?tab=readme-ov-file#yaml-format) to create
standard for creating `CHANGELOG.md` encourage developers to link associated tasks with given change. GitLab also 
provides tool to manage [changelogs](https://docs.gitlab.com/ee/user/project/changelogs.html).

### 1.1.3 Ensure any change to code receives approval of two strongly authenticated users (Automated)

Implemented at:

```
src/controls/code_changes/approval_required.py
```

[see](src/controls/code_changes/approval_required.py)

### 1.1.4 Ensure previous approvals are dismissed when updates are introduced to a code change proposal (Manual)

Implemented at:

```
src/controls/code_changes/approval_dismissed.py
```

[see](src/controls/code_changes/approval_dismissed.py)


### 1.1.5 Ensure there are restrictions on who can dismiss code change reviews (Manual)

I don't understand this rule or what should be checked to perform audit. Is it enough that
main branch is protected, noone can push to it and Developers and Maintainers can merge?

### 1.1.6 Ensure code owners are set for extra sensitive code or configuration (Manual)

Implemented at:

```
src/controls/code_changes/codeowners_file_exists.py
```

[see](src/controls/code_changes/codeowners_file_exists.py)


### 1.1.7 Ensure code owner's review is required when a change affects owned code (Manual)

Implemented at:

```
src/controls/code_changes/codeowners_approval.py
```

[see](src/controls/code_changes/codeowners_approval.py)


### 1.1.8 Ensure inactive branches are periodically reviewed and removed (Manual)

Implemented at:

```
src/controls/code_changes/stale_branches.py
```

[see](src/controls/code_changes/stale_branches.py)


### 1.1.9 Ensure all checks have passed before merging new code (Manual)

This rule also checks if `Pipelines must succeed (only_allow_merge_if_pipeline_succeeds)` is enabled.

What about `allow_merge_on_skipped_pipeline`? In some cases some BOTs use skipped pipelines to
perform some actions that would create recursive pipelines, and that's why skipped pipelines are useful.

Implemented at:

```
src/controls/code_changes/checks_have_passed_before_merging.py
```

[see](src/controls/code_changes/checks_have_passed_before_merging.py)

### 1.1.10 Ensure open Git branches are up to date before they can be merged into code base (Manual)

This rule also checks if `Enable merged results pipelines` and `Enable merge trains` is enabled.

Implemented at:

```
src/controls/code_changes/branches_are_up_to_date.py
```

[see](src/controls/code_changes/branches_are_up_to_date.py)

### 1.1.11 Ensure all open comments are resolved before allowing code change merging (Manual)

Implemented at:

```
src/controls/code_changes/open_comments_resolved_before_merge.py
```

[see](src/controls/code_changes/open_comments_resolved_before_merge.py)

### 1.1.12 Ensure verification of signed commits for new changes before merging (Manual)

GitLab uses `Merge Request` instead of `Pull Request` (wrong expression used in document)

Additionally, (besides `Reject unsigned commits`), GitLab allows to check:
- `Reject unverified users`
- `Reject inconsistent user name`
- `Check whether the commit author is a GitLab user`

Implemented at:

```
src/controls/code_changes/commit_user_verification.py
```

[see](src/controls/code_changes/commit_user_verification.py) 

### 1.1.13 Ensure linear history is required (Manual)

This rule should also check if `Squash commits when merging` is `Encourage` or `Require` to keep
main branch clean.

Implemented at:

```
src/controls/code_changes/linear_history.py
```

[see](src/controls/code_changes/linear_history.py)

### 1.1.14 Ensure branch protection rules are enforced for administrators (Manual)

Only available from Admin GUI.

### 1.1.15 Ensure pushing or merging of new code is restricted to specific individuals or teams (Manual)

This rule in this implementation checks following conditions: 
- Pushing should be set to `No One`
- Merging should be set to `Maintainers and Developers`

Maybe in future this tool will allow to define custom values for these rules to adjust to various companies polices

Implemented at:

```
src/controls/code_changes/pushing_or_merging_restriction.py
```

[see](src/controls/code_changes/pushing_or_merging_restriction.py)

### 1.1.16 Ensure force push code to branches is denied (Manual)

Implemented at:

```
src/controls/code_changes/force_push_denied.py
```

[see](src/controls/code_changes/force_push_denied.py)


### 1.1.17 Ensure branch deletions are denied (Manual)

Implemented at:

```
src/controls/code_changes/branch_deleteion_denied.py
```

[see](src/controls/code_changes/branch_deleteion_denied.py)

### 1.1.18 Ensure any merging of code is automatically scanned for risks (Manual)

Not implemented.

### 1.1.19 Ensure any changes to branch protection rules are audited (Manual)

Only available from Admin GUI.

### 1.1.20 Ensure branch protection is enforced on the default branch (Manual)

Implemented at:

```
src/controls/code_changes/default_branch_protected.py
```

[see](src/controls/code_changes/default_branch_protected.py)

## 1.2 Repository Management

### 1.2.1 Ensure all public repositories contain a SECURITY.md file (Manual)

Why this is only recommended for public repositories?

Implemented at:

```
src/controls/repository_management/security_file_available.py
```

[see](src/controls/repository_management/security_file_available.py)

### 1.2.2 Ensure repository creation is limited to specific members (Manual)

Only available from Admin GUI.

Creating repositories inside group requires Maintainer or Developer role?

Why this control audit and remediation are about `Sign-up restrictions` ?

### 1.2.3 Ensure repository deletion is limited to specific users (Manual)

Number of owners and maintainers is below 10 (TODO configure in future)

GitLab allows to change ability to delete project only to administrators.

https://docs.gitlab.com/ee/administration/settings/visibility_and_access_controls.html#restrict-project-deletion-to-administrators

Implemented at:

```
src/controls/repository_management/repository_deletion_limited.py
```

[see](src/controls/repository_management/repository_deletion_limited.py)

### 1.2.4 Ensure issue deletion is limited to specific users (Manual)

Implemented at:

```
src/controls/repository_management/issue_deletion_limited.py
```

[see](src/controls/repository_management/issue_deletion_limited.py)


### 1.2.5 Ensure all copies (forks) of code are tracked and accounted for (Manual)

This implementation allows no forks.

Implemented at:

```
src/controls/repository_management/repository_forks.py
```

[see](src/controls/repository_management/repository_forks.py)

