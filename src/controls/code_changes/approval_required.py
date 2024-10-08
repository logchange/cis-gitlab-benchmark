from src.controls.control import Control, ControlResult

REQUIRED_APPROVALS = 2


class ApprovalRequiredControl(Control):

    def get_name(self):
        return "1.1.3 Ensure any change to code receives approval of two strongly authenticated users (Automated)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        approval_rules = gl_project.approvalrules.list(lazy=False)

        default_branch = gl_project.default_branch

        passed = False
        more_info = ""

        # now, we check if there is a rule with value set to at least 2, but it can be 2 rules with different approval users
        # that requires for one approve, what also gives 2
        for rule in approval_rules:
            for protected_branch_by_rule in rule.protected_branches:
                if protected_branch_by_rule.name == default_branch:
                    if rule.approvals_required >= REQUIRED_APPROVALS and len(
                            protected_branch_by_rule.get('push_access_levels')) == 0:
                        passed = True
                        more_info = f"Required approvals: {rule.approvals_required}, and push to {default_branch} are disabled"
                    elif rule.approvals_required >= REQUIRED_APPROVALS:
                        passed = False
                        more_info = f"Required approvals: {rule.approvals_required}, BUT push to {default_branch} are enabled to {protected_branch_by_rule.get('push_access_levels')[0].get('access_level_description')}"

        return ControlResult(passed, more_info)
