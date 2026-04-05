import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def build_fuzzy_system():
    # New Antecedent/Consequent objects hold universe variables and membership functions
    attendance = ctrl.Antecedent(np.arange(0, 101, 1), 'attendance')
    assignment = ctrl.Antecedent(np.arange(0, 101, 1), 'assignment')
    test = ctrl.Antecedent(np.arange(0, 101, 1), 'test')
    
    performance = ctrl.Consequent(np.arange(0, 101, 1), 'performance')

    # Membership functions
    attendance.automf(3, names=['low', 'medium', 'high'])
    assignment.automf(3, names=['low', 'medium', 'high'])
    test.automf(3, names=['low', 'medium', 'high'])

    # Custom membership functions for performance
    performance['poor'] = fuzz.trimf(performance.universe, [0, 0, 50])
    performance['average'] = fuzz.trimf(performance.universe, [20, 50, 80])
    performance['good'] = fuzz.trimf(performance.universe, [50, 100, 100])

    # Rules
    rule1 = ctrl.Rule(attendance['low'] & test['low'], performance['poor'])
    rule2 = ctrl.Rule(attendance['high'] & test['high'], performance['good'])
    rule3 = ctrl.Rule(assignment['high'] & test['high'], performance['good'])
    rule4 = ctrl.Rule(attendance['medium'] & test['medium'], performance['average'])
    rule5 = ctrl.Rule(attendance['low'] & assignment['low'], performance['poor'])
    rule6 = ctrl.Rule(attendance['high'] & assignment['medium'] & test['medium'], performance['average'])
    rule7 = ctrl.Rule(attendance['high'] & assignment['high'] & test['medium'], performance['good'])
    rule8 = ctrl.Rule(attendance['low'] & assignment['high'] & test['high'], performance['average'])
    rule9 = ctrl.Rule(test['low'] & assignment['low'], performance['poor'])

    perf_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    perf_sim = ctrl.ControlSystemSimulation(perf_ctrl)
    
    return perf_sim

fuzzy_sim = build_fuzzy_system()

def compute_fuzzy_score(attendance_val, assignment_val, test_val):
    fuzzy_sim.input['attendance'] = attendance_val
    fuzzy_sim.input['assignment'] = assignment_val
    fuzzy_sim.input['test'] = test_val
    
    try:
        fuzzy_sim.compute()
        return fuzzy_sim.output['performance']
    except Exception as e:
        return 50.0 # fallback
