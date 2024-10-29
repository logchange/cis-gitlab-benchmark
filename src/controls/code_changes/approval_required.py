from src.controls.control import Control, ControlResult


class ApprovalRequiredControl(Control):

    def __init__(self, config: dict):
        control_dict = config.get('gitlab').get('code_changes').get('approval_required')
        enabled = control_dict.get('enabled')
        super().__init__(enabled)
        self.required_approvals = control_dict.get('required_approvals')

    def get_name(self):
        return f"1.1.3 Ensure any change to code receives approval of {self.required_approvals} strongly authenticated users (Automated)"

    def validate_specific(self, gl_group_project, gl_project) -> ControlResult | None:
        approval_rules = gl_project.approvalrules.list(lazy=False)

        protected_branches_result = {}

        for protected_branch in gl_project.protectedbranches.list():
            protected_branches_result[protected_branch.name] = {'passed': False, 'more_info': ""}

        # now, we check if there is a rule with value set to at least 2, but it can be 2 rules with different approval users
        # that requires for one approve, what also gives 2
        for rule in approval_rules:
            for protected_branch_by_rule in rule.protected_branches:
                if protected_branch_by_rule.get('name') in protected_branches_result.keys():
                    branch_name = protected_branch_by_rule.get('name')
                    if rule.approvals_required >= self.required_approvals and len(
                            protected_branch_by_rule.get('push_access_levels')) == 1 and \
                            protected_branch_by_rule.get('push_access_levels')[0].get('access_level') == 0:
                        passed = True
                        more_info = f"Required approvals: {rule.approvals_required}, and push to {branch_name} are disabled"
                    elif rule.approvals_required >= self.required_approvals:
                        passed = False
                        more_info = f"Required approvals: {rule.approvals_required}, BUT push to {branch_name} are enabled to {protected_branch_by_rule.get('push_access_levels')[0].get('access_level_description')}"
                    else:
                        passed = False
                        more_info = ""
                    protected_branches_result[branch_name] = {'passed': passed, 'more_info': more_info}

        final_passed = True
        final_more_info = ""

        for branch_name in protected_branches_result.keys():
            if not protected_branches_result[branch_name]['passed']:
                final_passed = False
            final_more_info += protected_branches_result[branch_name]['more_info']

        return ControlResult(self.get_name(), final_passed, final_more_info)
