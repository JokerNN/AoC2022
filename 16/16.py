import re
from functools import cache
from typing import List, Any, Dict, FrozenSet
from dataclasses import dataclass
from utils.inputs import get_input_lines

parsing_re = re.compile(r'Valve (?P<valve_id>\w\w) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valve(s)? (?P<conns>.+)')

@dataclass(frozen=True)
class Valve:
    id: str
    flow_rate: int
    conns: List[str]


valves: Dict[str, Valve] = {}
all_score_valves: FrozenSet[str] = frozenset()

@cache
def rec(open_valves: FrozenSet[str], cur_valve: str, minute: int, score: int):
    if minute == 0:
        return score

    if open_valves == all_score_valves:
        return score

    open_score = score
    valve_score = valves[cur_valve].flow_rate
    if cur_valve not in open_valves and valve_score > 0:
        total_open_score = minute * valves[cur_valve].flow_rate
        open_score += rec(open_valves | frozenset([cur_valve]), cur_valve, minute - 1, score + total_open_score)

    go_scores = []
    for conn in valves[cur_valve].conns:
        go_scores.append(rec(open_valves, conn, minute - 1, score))
        
    return max([open_score, *go_scores])

    

def main():
    global all_score_valves
    for line in get_input_lines('./input_tst.txt'):
        m = parsing_re.match(line)
        if m is None:
            raise Exception('Bad input')

        valve_id = m.group('valve_id')
        flow_rate = int(m.group('flow_rate'))
        conns = m.group('conns').split(', ')
        valves[valve_id] = Valve(valve_id, flow_rate, conns)

    all_score_valves = frozenset(valve.id for valve in valves.values() if valve.flow_rate > 0)
    
    res = rec(frozenset(), 'AA', 30, 0)
    print(res)

if __name__ == '__main__':
    main()
    