from src.controls.control import Control, ControlResult


class CodeOwnersApprovalRequiredControl(Control):

    def get_name(self):
        return "1.1.7 Ensure code owner's review is required when a change affects owned code (Manual)"

    def validate(self, gl_group_project, gl_project) -> ControlResult:
        approval_rules = gl_project.approvalrules.list(lazy=False)

        protected_branches_result = {}

        for protected_branch in gl_project.protectedbranches.list():
            protected_branches_result[protected_branch.name] = {'passed': False, 'more_info': ""}

        for rule in approval_rules:
            for protected_branch_by_rule in rule.protected_branches:
                if protected_branch_by_rule.get('name') in protected_branches_result.keys():
                    branch_name = protected_branch_by_rule.get('name')
                    if protected_branch_by_rule.get('code_owner_approval_required'):
                        passed = True
                        more_info = ""
                    else:
                        passed = False
                        more_info = f"For branch {branch_name} no code owners approval required"
                    protected_branches_result[branch_name] = {'passed': passed, 'more_info': more_info}

        final_passed = True
        final_more_info = ""

        for branch_name in protected_branches_result.keys():
            if not protected_branches_result[branch_name]['passed']:
                final_passed = False
            final_more_info += protected_branches_result[branch_name]['more_info']

        return ControlResult(self.get_name(), final_passed, final_more_info)
