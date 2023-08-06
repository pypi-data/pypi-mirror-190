from ..functions import create_graph, write_spec_details
from .image import load_svg_graphviz


def write_behavioral_actions(write_directory, report_name, actions_to_map, behavioral_action_space,
                             all_edges, policies, mechanisms, description_sets, policy_options):
    all_nodes, graph = create_graph(actions_to_map, report_name, behavioral_action_space, all_edges,
                                    return_graph=True)
    html = write_spec_details(all_nodes,
                              behavioral_action_space, policies, mechanisms, description_sets, policy_options)
    svg = load_svg_graphviz(graph)

    with open("{}/{}.html".format(write_directory, report_name), "w") as f:
        f.write(svg)
        f.write(html)
