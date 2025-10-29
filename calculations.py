import streamlit as st
# --- Utility Functions


def get_achievement_pct(achieved, budget):
    return achieved / (budget if budget != 0 else 1)


def get_per_unit_incentive(pct, l1: int, l2=int, l3=int):
    if pct > 1.5:
        return l3
    elif pct > 1.0:
        return l2
    elif pct >= 0.8:
        return l1
    return 0


def calculate_incentive(inputs, designation, responsibility):
    # Unpack inputs
    achieved = inputs['achieved']
    budget = inputs['budget']
    resale_achieved = inputs['resale_achieved']
    resale_budget = inputs['resale_budget']

    ''' for early invoice '''
    # temp_invoice = inputs['temp_invoice']

    ''' Step 1: Core % '''
    pct = get_achievement_pct(achieved, budget)
    unit_incentive = get_per_unit_incentive(pct, 3000, 4000, 5000)

    # for resale
    resale_pct = get_achievement_pct(resale_achieved, resale_budget)
    resale_unit_incentive = get_per_unit_incentive(
        resale_pct, 2000, 3000, 4500)

    ''' Step 2: Type of sales (cash/credit)'''
    dp_incentive = inputs['dp30'] * 1000 + inputs['dp50'] * 1500
    cash_incentive = inputs['cash'] * 6000

    # for resale
    resale_dp_incentive = inputs['Resale_dp30'] * \
        1000 + inputs['Resale_dp50'] * 1500
    resale_cash_incentive = inputs['Resale_cash'] * 4000

    ''' Step 3: Basic Incentive '''
    base_incentive_new = achieved * unit_incentive + dp_incentive + cash_incentive
    base_incentive_resale = resale_achieved * resale_unit_incentive + \
        resale_dp_incentive + resale_cash_incentive

    base_incentive = base_incentive_new + base_incentive_resale

    ''' Step 4: Add-ons '''
    add_ons = (
        # inputs['rx_supreme'] * 5000 +
        inputs['zero_sales'] * 1000 +
        inputs['installment'] * 1000
    )

    penalty = inputs['credit'] * 1000 + \
        inputs['new_inquiry'] * abs(unit_incentive - 1000) + \
        inputs['resale_inquiry'] * abs(resale_unit_incentive - 1000)
    total_before_mult = base_incentive + add_ons - penalty

    # Step 4: Multiplier logic
    multiplier = 1.0
    # if designation == "Territory officer":
    #     if pct >= 1.75 and resale_achieved >= resale_budget + 1:
    #         multiplier = 2.0
    #     elif pct >= 1.6 and resale_achieved >= resale_budget + 1:
    #         multiplier = 1.5
    #     elif pct >= 1.4 and resale_achieved >= resale_budget + 1:
    #         multiplier = 1.25
    # else:
    #     if pct >= 1.65 and resale_achieved >= resale_budget + 1:
    #         multiplier = 2.0
    #     elif pct >= 1.5 and resale_achieved >= resale_budget + 1:
    #         multiplier = 1.5
    #     elif pct >= 1.3 and resale_achieved >= resale_budget + 1:
    #         multiplier = 1.25

    # Step 5: Designation logic
    if designation == "Area Head":
        if inputs['responsibility'] == "Complete Responsibility":
            sup_level_incentive = 1
            total_adjusted = total_before_mult * sup_level_incentive

        elif inputs['responsibility'] == "Direct Supervised Responsibility" and st.session_state.supervised_target == False:
            sup_level_incentive = 0.4
            total_adjusted = total_before_mult * sup_level_incentive

        elif inputs['responsibility'] == "Direct Supervised Responsibility" and st.session_state.supervised_target == True:
            sup_level_incentive = 0.5
            total_adjusted = total_before_mult * sup_level_incentive

        else:  # Additional Supervised Responsibility
            sup_level_incentive = 0.3
            total_adjusted = total_before_mult * sup_level_incentive
    else:
        total_adjusted = total_before_mult

    final = total_adjusted * multiplier

    return {
        "unit_incentive": unit_incentive,
        "resale_incentive": resale_unit_incentive,
        # "early_bonus": early_bonus,
        "base_incentive": base_incentive,
        "add_ons": add_ons,
        "penalty": penalty,
        "total_before_mult": total_before_mult,
        "total_adjusted": total_adjusted,
        "multiplier": multiplier,
        "final": final
    }
