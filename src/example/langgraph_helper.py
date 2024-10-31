import os.path

from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles


def graph_to_png(graph, file_name: str):
    image_data = graph.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )

    with open(os.path.join("..", file_name), "wb") as f:
        f.write(image_data)