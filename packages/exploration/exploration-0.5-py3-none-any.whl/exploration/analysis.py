"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-24
- Purpose: Analysis functions for decision graphs an explorations.
"""
#
#    """
#    Should we include annotations in the progress description?
#    1. Include
#    2. Exclude
#    3. Mention but don't print full annotation
#    TODO: Have an extra parameter for this
#
#    Example:
#    >>> import pytest
#    >>> pytest.xfail("Not implemented yet.")
#    >>> e = journal.convertJournal('''\\
#    ... S pit Start
#    ... A gain jump
#    ... A gain attack
#    ... n button check
#    ... zz Wilds
#    ... o up
#    ...   q _flight
#    ... o left
#    ... x left left_nook right
#    ... a geo_rock
#    ...   At gain geo*15
#    ...   At deactivate
#    ... o up
#    ...   q _tall_narrow
#    ... t right
#    ... o right
#    ...   q attack
#    ... ''')
#    >>> for line in describeProgress(e).splitlines():
#    ...    print(line)
#    Start of the exploration
#    You are in the zone Start
#    You are in the region Wilds
#    You are at the pit
#    You gain the power 'jump'
#    You gain the power 'attack'
#    One note at this step
#    There are transitions:
#        left (leads to unknown)
#        up (leads to unknown; requires _flight)
#    You explore transition left to find the left_nook.
#    There are transitions:
#        right (leads to pit)
#        up (requires _tall_narrow)
#    There are actions:
#        geo_rock (gain geo*15; deactivate)
#    You retrace the transition 'right'
#    You are at the pit.
#    There are transitions:
#        left (leads to the left_nook)
#        up (leads to unknown; requires _flight)
#        right (leads to unknown; requries attack)
#    """
#    # TODO: write code here to make the example above come true.
#    # You will want to make use of a loop that runs through the
#    # different steps of the exploration object (the len function will
#    # tell you how many steps it has).
#    # You will need to access the current graph (or maybe also the
#    # current game state) through the situationAtStep (or maybe also
#    # stateAtStep) method, and the positionAtStep and transitionAtStep
#    # methods will also come in handy. In fact, the situationAtStep
#    # method combines those so it may be more convenient.
#    # If you want a challenge, try to use type annotations so that the
#    # Thonny assistant shows no errors, but don't worry about the
#    # assistant if that's too complicated.
#    # The destinationsFrom method of a DecisionGraph will come in handy
#    # (it's actually defined in graphs.py as part of the
#    # UniqueExitsGraph class).

from typing import List, Tuple

from exploration import core, journal


babyJournal = """
S Start
A gain jump
A gain attack
n button check
zz Wilds
o up
q _flight
o left
x left left_nook right
a geo_rock
At gain geo*15
At deactivate
o up
q _tall_narrow
t right
o right
q attack
"""
babyJournal2 = """
S Start
A gain jump
A gain attack
n button check
zz Wilds
o up
q _flight
o left
x left left_nook right
"""

e1 = journal.convertJournal(babyJournal)
e2 = journal.convertJournal(babyJournal2)


def describeProgress(exploration: core.Exploration) -> str:
    """
    Describes the progress of an exploration by noting each room/zone
    visited and explaining the options visible at each point plus which
    option was taken. Notes powers/tokens gained/lost along the way.
    """
    # allTransitionsList: List[core.Transition] = []
    # allDecisionsList: List[core.Decision] = []

    s: str = "description of progress"

    print(exploration.situationAtStep(0))
    currTransition = exploration.getTransitionAtStep(0)
    print(currTransition)
    print("You are in the starting zone \n")

    for i in range(1, len(exploration)):
        situation = exploration.situationAtStep(i)

        #print(situation)
        for ann in situation.annotations:
            print("Annotation: " + ann)

        currDecision = situation.position
        print("Decision: " + currDecision)

        currTransition = situation.transition
        if currTransition is not None:
            print("Transition: " + currTransition)

        currGraph = situation.graph

        try:
            currEffects = currGraph.getTransitionEffects(
                currDecision,
                currTransition
            )
        except KeyError:
            currEffects = None

        if currEffects is not None:
            print("Effects:", currEffects)

        print("State:", situation.state)

        print()

    return s


# we running (our code)
describeProgress(e1)

# Peter's old code sketch

#    for i in range(len(exploration)):
#        (
#            now,  # current graph
#            here,  # current position
#            state,  # current game state
#            taken,  # transition taken (FROM this step)
#            notes  # annotations on this step
#        ) = exploration.situationAtStep(i)
#
#        level1Zones = [
#            z
#            for z in now.zoneAncestors(here)
#            if now.zoneHierarchyLevel(z) == 1
#        ]
#
#        newLevel1 = level1Zones - prevLevel1Zones
#
#
#        prev = now
#        prevDecision = here
#        prevState = state
#        prevTaken = taken
#        prevLevel1Zones = level1Zones


def unexploredBranches(
    graph: core.DecisionGraph
) -> List[Tuple[core.Decision, core.Transition]]:
    """
    Returns a list of from-decision, transition-at-that-decision pairs
    which each identify an unexplored branch in the given graph.

    TODO: Separate by blocked- vs. unblocked & add logic to detect
    trivially-unblocked edges?
    """
    result = []
    for (src, dst, transition) in graph.edges(keys=True):
        # Check if this edge goes from a known to an unknown node
        if not graph.isUnknown(src) and graph.isUnknown(dst):
            result.append((src, transition))
    return result


def unexploredBranchesPerStep(expl: core.Exploration) -> List[int]:
    """
    Takes an exploration object and computes the number of unexplored
    branches at each step, returning a list of integers.
    """
    result = []
    for i in range(len(expl)):
        result.append(len(unexploredBranches(expl.graphAtStep(i))))
    return result
