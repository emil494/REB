from typing import Set

from pm4py.objects.dcr.hierarchical.obj import HierarchicalDcrGraph
from pm4py.objects.dcr.obj import DcrGraph
from pm4py.objects.dcr.semantics import DcrSemantics

class NestedDcrGraph(DcrSemantics):
    
    @staticmethod
    def find_all(cls, graph, event):
        res = set()
        if event not in graph.nestedgroups.keys():
            res.add(event)
        else:
            events = graph.nestedgroups[event]
            
            for e in events:
                res= res.union(cls.find_all(cls, graph, e))
      
        return res
            
    
    @classmethod
    def enabled(cls, graph) -> Set[str]:
        res = super().enabled(graph)
        for g in graph.nestedgroups.keys():
            if not g in res and g in graph.conditions.keys():
                all = cls.find_all(cls, graph, g)
                for e in all:
                    if e in res:
                        res.discard(e)
            res.discard(g)

        return res
    
    @classmethod
    def execute(cls, graph, event):
        if event in graph.marking.pending:
            if event in graph.nestedgroups.keys():
                raise TypeError('A pending nested group head cannot be executed')
            graph.marking.pending.discard(event)
        graph.marking.executed.add(event)
        
        # Excludes
        if event in graph.excludes:
            for e_prime in graph.excludes[event]:
                all = cls.find_all(cls, graph, e_prime)
                for e in graph.marking.included.intersection(all):
                    graph.marking.included.discard(e)

        # Includes
        if event in graph.includes:
            for e_prime in graph.includes[event]:
                all = cls.find_all(cls, graph, e_prime)
                graph.marking.included.add(e_prime)
                for e in (all):
                    graph.marking.included.add(e)

        # Response
        if event in graph.responses:
            for e_prime in graph.responses[event]:
                all = cls.find_all(cls, graph, e_prime)
                graph.marking.pending.update(all)

        for key, values in graph.nestedgroups.items():
            if event in values:
                cls.execute(graph,key)
        
        return graph

