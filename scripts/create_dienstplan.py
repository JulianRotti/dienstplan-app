import pandas as pd
import networkx as nx

def convert_to_nodes(df1, df2, df3):
    processes = list(df1.columns)[2:]
    days = list(df2.columns)[2:]

    # Step 1: Identify available processes for each employee
    worker_skills = []
    for index, row in df1.iterrows():
        for index2, row2 in df2.iterrows():
            name = row['Mitarbeiter']
            available_processes = tuple([process for process in processes if row[process] == 'Ja'])
            if len(available_processes)>0 and name == row2['Mitarbeiter']:
                for available_day in [day for day in days if row2[day] == 'Ja']:
                    worker_skills.append({"name": name, "Prozess": available_processes, "Tag": available_day})

    processes_needed = []
    iterator = 0
    for index, row in df3.iterrows():
        process = row['Prozesse']
        for day in days:
            process_multiplicity = row[day]
            for i in range(0, process_multiplicity):
                processes_needed.append({"id": iterator, "Prozess": process, "Tag": day})
                iterator+=1

    hashable_nodes_A = [frozenset(node.items()) for node in worker_skills]
    hashable_nodes_B = [frozenset(node.items()) for node in processes_needed]

    return hashable_nodes_A, hashable_nodes_B

def find_maximal_matching(df1, df2, df3):
    hashable_nodes_A, hashable_nodes_B = convert_to_nodes(df1, df2, df3)

    # Create a bipartite graph
    B = nx.Graph()

    # Add the hashable nodes to the graph
    B.add_nodes_from(hashable_nodes_A, bipartite=0)
    B.add_nodes_from(hashable_nodes_B, bipartite=1)

    # Add edges
    for hashable_a in hashable_nodes_A:
        for hashable_b in hashable_nodes_B:
            # Convert frozensets back to dictionaries to compare values
            dict_a = dict(hashable_a)
            dict_b = dict(hashable_b)

            if dict_a["Tag"] == dict_b["Tag"] and dict_b["Prozess"] in dict_a["Prozess"]:
                B.add_edge(hashable_a, hashable_b)

    # Initialize DataFrame
    final_plan = pd.DataFrame(columns=['Tag', 'Mitarbeiter', 'Prozess'])

    # Find global maximal matching of B
    matching = nx.max_weight_matching(B)

    # Find nodes which are not included in the maximal matching 
    # Convert matching to a set of nodes
    matched_nodes = set()
    for edge in matching:
        matched_nodes.add(edge[0])
        matched_nodes.add(edge[1])

    # Convert hashable_nodes_A and hashable_nodes_B to sets
    set_hashable_nodes_A = set(hashable_nodes_A)
    set_hashable_nodes_B = set(hashable_nodes_B)

    # Find nodes not in matching
    unmatched_nodes_A = set_hashable_nodes_A - matched_nodes
    unmatched_nodes_B = set_hashable_nodes_B - matched_nodes

    for node in unmatched_nodes_A:
        new_row = pd.DataFrame({"Tag": dict(node)["Tag"], "Prozess": 'N/A', "Mitarbeiter": dict(node)["name"]}, index=[0])
        final_plan = pd.concat([final_plan, new_row])

    for node in unmatched_nodes_B:
        new_row = pd.DataFrame({"Tag": dict(node)["Tag"], "Prozess": dict(node)["Prozess"], "Mitarbeiter": 'N/A'}, index=[0])
        final_plan = pd.concat([final_plan, new_row])

    for edge in matching:
        try:
            name = dict(edge[1])["name"]
            process = dict(edge[0])["Prozess"]
            day = dict(edge[0])["Tag"]
        except KeyError:
            name = dict(edge[0])["name"]
            process = dict(edge[1])["Prozess"]
            day = dict(edge[1])["Tag"]
        
        new_row = pd.DataFrame({"Tag": day, "Prozess": process, "Mitarbeiter": name}, index=[0])
        final_plan = pd.concat([final_plan, new_row])

    return final_plan