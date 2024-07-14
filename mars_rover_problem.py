import logging
from typing import List
from aimacode.planning import Action
from aimacode.utils import expr
from aimacode.logic import PropKB
from planning_problem import BasePlanningProblem
from _utils import decode_state, FluentState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarsRoverProblem(BasePlanningProblem):
    def __init__(self):
        locations = ["Base", "Location1", "Location2"]
        initial_pos = [
            expr("At(Base)"),
            expr("SampleAvailable(Location1)"),
            expr("PhotoOpportunity(Location2)"),
            expr("RockAvailable(Location2)"),
            expr("SoilAvailable(Location1)"),
        ]
        initial_neg = [
            expr("Sample(Collected)"),
            expr("Photo(Taken)"),
            expr("Data(Transmitted)"),
            expr("Rock(Analyzed)"),
            expr("Soil(Analyzed)"),
        ]

        for loc in locations:
            if loc != "Base":
                initial_neg.append(expr(f"At({loc})"))

        goals = [
            expr("Sample(Collected)"),
            expr("Photo(Taken)"),
            expr("Data(Transmitted)"),
            expr("Rock(Analyzed)"),
            expr("Soil(Analyzed)"),
        ]

        initial_state = FluentState(initial_pos, initial_neg)
        super().__init__(initial_state, goals)
        self.actions_list = self.get_actions()

    def get_actions(self) -> List[Action]:
        """Return a list of Action objects defining the valid actions for the problem."""

        def move_actions():
            moves = []
            locations = ["Base", "Location1", "Location2"]
            for loc_from in locations:
                for loc_to in locations:
                    if loc_from != loc_to:
                        precond_pos = [expr(f"At({loc_from})")]
                        precond_neg = []
                        effect_add = [expr(f"At({loc_to})")]
                        effect_rem = [expr(f"At({loc_from})")]
                        move = Action(
                            expr(f"Move({loc_from}, {loc_to})"),
                            [precond_pos, precond_neg],
                            [effect_add, effect_rem],
                        )
                        moves.append(move)
            return moves

        def collect_sample_actions() -> List[Action]:
            """Return a list of Action objects for collecting samples."""
            precond_pos = [expr("At(Location1)"), expr("SampleAvailable(Location1)")]
            precond_neg = []
            effect_add = [expr("Sample(Collected)")]
            effect_rem = [expr("SampleAvailable(Location1)")]
            collect_sample = Action(
                expr("CollectSample(Location1)"),
                [precond_pos, precond_neg],
                [effect_add, effect_rem],
            )
            return [collect_sample]

        def take_photo_actions() -> List[Action]:
            """Return a list of Action objects for taking photos."""
            precond_pos = [expr("At(Location2)"), expr("PhotoOpportunity(Location2)")]
            precond_neg = []
            effect_add = [expr("Photo(Taken)")]
            effect_rem = [expr("PhotoOpportunity(Location2)")]
            take_photo = Action(
                expr("TakePhoto(Location2)"),
                [precond_pos, precond_neg],
                [effect_add, effect_rem],
            )
            return [take_photo]

        def analyze_rock_actions() -> List[Action]:
            """Return a list of Action objects for analyzing rocks."""
            precond_pos = [expr("At(Location2)"), expr("RockAvailable(Location2)")]
            precond_neg = []
            effect_add = [expr("Rock(Analyzed)")]
            effect_rem = [expr("RockAvailable(Location2)")]
            analyze_rock = Action(
                expr("AnalyzeRock(Location2)"),
                [precond_pos, precond_neg],
                [effect_add, effect_rem],
            )
            return [analyze_rock]

        def analyze_soil_actions() -> List[Action]:
            """Return a list of Action objects for analyzing soil."""
            precond_pos = [expr("At(Location1)"), expr("SoilAvailable(Location1)")]
            precond_neg = []
            effect_add = [expr("Soil(Analyzed)")]
            effect_rem = [expr("SoilAvailable(Location1)")]
            analyze_soil = Action(
                expr("AnalyzeSoil(Location1)"),
                [precond_pos, precond_neg],
                [effect_add, effect_rem],
            )
            return [analyze_soil]

        def transmit_data_actions() -> List[Action]:
            """Return a list of Action objects for transmitting data."""
            precond_pos = [
                expr("Sample(Collected)"),
                expr("Photo(Taken)"),
                expr("Rock(Analyzed)"),
                expr("Soil(Analyzed)"),
            ]
            precond_neg = []
            effect_add = [expr("Data(Transmitted)")]
            effect_rem = []
            transmit_data = Action(
                expr("TransmitData"),
                [precond_pos, precond_neg],
                [effect_add, effect_rem],
            )
            return [transmit_data]

        return (
            move_actions()
            + collect_sample_actions()
            + take_photo_actions()
            + analyze_rock_actions()
            + analyze_soil_actions()
            + transmit_data_actions()
        )

    def actions(self, state) -> List[Action]:
        """Return the actions that can be executed in the given state."""
        possible_actions = []
        fs = decode_state(state, self.state_map)
        kb = PropKB()
        for clause in fs.pos:
            kb.tell(clause)
        for action in self.actions_list:
            if action.check_precond(kb, action.args):
                possible_actions.append(action)
        logger.info(f"Current state: {fs.pos}, {fs.neg}")
        logger.info(f"Possible actions: {possible_actions}")
        return possible_actions

    def result(self, state, action) -> tuple:
        """Return the state that results from executing the given action in the given state."""
        new_state = list(state)
        for effect in action.effect_add:
            new_state[self.state_map.index(effect)] = True
        for effect in action.effect_rem:
            new_state[self.state_map.index(effect)] = False
        logger.info(
            f"Action: {action}, New state: {decode_state(tuple(new_state), self.state_map).pos}"
        )
        return tuple(new_state)

    def goal_test(self, state) -> bool:
        fs = decode_state(state, self.state_map)
        for goal in self.goal:
            if goal not in fs.pos:
                return False
        return True
