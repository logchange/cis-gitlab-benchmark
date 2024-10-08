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