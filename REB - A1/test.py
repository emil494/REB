#%load_ext autoreload
#%autoreload 2

import numpy as np
import os
import pandas as pd
import pm4py
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.visualization.petri_net import visualizer as pn_visualizer

print(os.getcwd())
to_run = True
if to_run:
    os.chdir('..')
    to_run = False
print(os.getcwd())

# Create a Petri net
net = PetriNet("petri_net_rules_1_to_8")

# Create transitions
t_fill_out_application = PetriNet.Transition("t_fill_out_application", "Fill out application")
t_architect_review = PetriNet.Transition("t_architect_review", "Architect Review")
t_lawyer_review = PetriNet.Transition("t_lawyer_review", "Lawyer Review")
t_reject = PetriNet.Transition("t_reject", "Reject")
t_applicant_informed = PetriNet.Transition("t_applicant_informed", "Applicant informed")
t_change_phase_to_abort = PetriNet.Transition("t_change_phase_to_abort", "Change phase to Abort")
t_change_phase_to_payout = PetriNet.Transition("t_change_phase_to_payout", "Change Phase to Payout")
t_first_payment = PetriNet.Transition("t_first_payment", "First payment")
t_undo_payment = PetriNet.Transition("t_undo_payment", "Undo payment")
t_change_phase_to_end_report = PetriNet.Transition("t_change_phase_to_end_report", "Change Phase to End Report")
t_change_phase_to_end_report2 = PetriNet.Transition("t_change_phase_to_end_report", "Change Phase to End Report")

t_account_number_changed = PetriNet.Transition("t_account_number_changed", "Account number changed")
t_approve_changed_account = PetriNet.Transition("t_approve_changed_account", "Approve changed account")
t_execute_abandon = PetriNet.Transition("t_execute_abandon", "Execute abandon")
t_change_phase_to_abandon = PetriNet.Transition("t_change_phase_to_abandon", "Change phase to Abandon")

net.transitions.add(t_fill_out_application)
net.transitions.add(t_architect_review)
net.transitions.add(t_lawyer_review)
net.transitions.add(t_reject)
net.transitions.add(t_applicant_informed)
net.transitions.add(t_change_phase_to_abort)
net.transitions.add(t_change_phase_to_payout)
net.transitions.add(t_first_payment)
net.transitions.add(t_undo_payment)
net.transitions.add(t_change_phase_to_end_report)
net.transitions.add(t_change_phase_to_end_report2)
net.transitions.add(t_account_number_changed)
net.transitions.add(t_approve_changed_account)
net.transitions.add(t_execute_abandon)
net.transitions.add(t_change_phase_to_abandon)

# Create places
p1 = PetriNet.Place("p1")
p2 = PetriNet.Place("p2")
p3 = PetriNet.Place("p3")
p4 = PetriNet.Place("p4")
p5 = PetriNet.Place("p5")
p6 = PetriNet.Place("p6")
p7 = PetriNet.Place("p7")
p8 = PetriNet.Place("p8")
p9 = PetriNet.Place("p9")


net.places.add(p1)
net.places.add(p2)
net.places.add(p3)
net.places.add(p4)
net.places.add(p5)
net.places.add(p6)
net.places.add(p7)
net.places.add(p8)
net.places.add(p9)

# Create arcs
petri_utils.add_arc_from_to(p1, t_fill_out_application, net)
petri_utils.add_arc_from_to(t_fill_out_application, p3, net)
petri_utils.add_arc_from_to(p3, t_lawyer_review, net)
petri_utils.add_arc_from_to(p3, t_architect_review, net)
petri_utils.add_arc_from_to(t_architect_review, p2, net)
petri_utils.add_arc_from_to(t_lawyer_review, p2, net)
petri_utils.add_arc_from_to(t_reject, p5, net)
petri_utils.add_arc_from_to(p5, t_applicant_informed, net)
petri_utils.add_arc_from_to(t_applicant_informed, p6, net)
petri_utils.add_arc_from_to(p6, t_change_phase_to_abort, net)
petri_utils.add_arc_from_to(p2, t_reject, net)
petri_utils.add_arc_from_to(p2, t_change_phase_to_payout, net)
petri_utils.add_arc_from_to(t_first_payment, p4, net)
petri_utils.add_arc_from_to(p4, t_undo_payment, net)
petri_utils.add_arc_from_to(t_undo_payment, p2, net)
petri_utils.add_arc_from_to(p2, t_account_number_changed, net)
petri_utils.add_arc_from_to(t_account_number_changed, p7, net)
petri_utils.add_arc_from_to(p7, t_approve_changed_account, net)
petri_utils.add_arc_from_to(t_approve_changed_account, p2, net)
petri_utils.add_arc_from_to(t_change_phase_to_payout, p8, net)
petri_utils.add_arc_from_to(p8, t_first_payment, net)
petri_utils.add_arc_from_to(t_change_phase_to_abort, p9, net)

petri_utils.add_arc_from_to(p2, t_change_phase_to_end_report, net)
petri_utils.add_arc_from_to(p4, t_change_phase_to_end_report2, net)
petri_utils.add_arc_from_to(t_change_phase_to_end_report2, p9, net)
petri_utils.add_arc_from_to(t_change_phase_to_end_report, p9, net)


#Add rules 2-8 to the Petri net
# TODO


# Initial and final markings
# TODO: update as needed.
initial_marking = Marking()
initial_marking[p1] = 1

final_marking = Marking()
final_marking[p9] = 1

# Visualize the Petri net
gviz = pn_visualizer.apply(net, initial_marking, final_marking)
pn_visualizer.view(gviz)