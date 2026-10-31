"""Build data/proposals_v2.yaml: the 100 bills with the most loaded wording made plainer."""

import yaml

REWORDS = {
    "edu_loan_forgive": "Cancel up to $20,000 in federal student loans for borrowers earning under $125,000.",
    "soc_work_requirements": "Require adults aged 18 to 54 without dependents, unless exempt for disability, to work 20 hours a week to receive food assistance.",
    "soc_paid_leave": "Provide 12 weeks of paid family leave, funded by a payroll contribution.",
    "soc_religious_exempt": "Let businesses decline services that conflict with the owner's religious beliefs.",
    "health_public_option": "Create a public health insurance plan available to all residents as an option alongside private plans.",
    "health_single_payer": "Replace private health insurance with one public plan covering all residents.",
    "health_abortion_ban": "Prohibit abortion after 15 weeks of pregnancy, with an exception when the patient's life is at risk.",
    "health_abortion_protect": "Make abortion legal nationwide up to fetal viability.",
    "imm_pathway": "Create a path to citizenship for undocumented immigrants who arrived as minors.",
    "soc_gender_sports": "Require athletes in school sports to compete on teams matching the sex recorded at their birth.",
    "guns_assault_ban": "Prohibit the sale of semi-automatic rifles with detachable magazines.",
    "tax_child_credit": "Increase the child tax credit to $3,000 per child, and pay it in full to families who owe no income tax.",
}

with open("data/proposals_100.yaml") as handle:
    bills = yaml.safe_load(handle)
for bill in bills:
    bill["text"] = REWORDS.get(bill["id"], bill["text"])
assert len(bills) == 100 and all(key in {b["id"] for b in bills} for key in REWORDS)
with open("data/proposals_v2.yaml", "w") as handle:
    handle.write("# Reworded from proposals_100.yaml. topic and lean are for analysis only and are never shown to models.\n")
    yaml.safe_dump(bills, handle, sort_keys=False, width=1000)
print(f"{len(bills)} bills, {len(REWORDS)} reworded")
