import networkx as nx
import matplotlib.pyplot as plt
import json
import requests


def draw_nx(filename):
    describegraph = open(filename + ".json", "r")
    lngraph = json.load(describegraph)
    # print(lngraph["edges"]['node1_pub'][0])
    # Construct network graph
    graph = nx.Graph()

    # Add edges and nodes
    for edge in lngraph["edges"]:
        # Name the nodes by last 4 characters of node ID
        node1 = edge["node1_pub"][-4:]
        node2 = edge["node2_pub"][-4:]

        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_edge(node1, node2)

    # Show graph info before reduction

    # Remove nodes with fewer than 3 channels to make graph cleaner
    remove = [node for node, degree in dict(graph.degree()).items() if degree < 3]
    graph.remove_nodes_from(remove)

    # Show graph info after reduction

    # Set figure/diagram options (thin grey lines for channels, black dots for nodes)

    # 16:9 image ratio
    fig = plt.figure(figsize=(16, 9))

    # Spring layout arranges nodes automatically.
    # Channels cause "attraction" (spring), nodes cause "repulsion" (opposite)
    # k controls distance between nodes. Spread them out to make graph less dense
    # Seed for reproducible layout
    # pos = nx.spring_layout(graph, k=0.4, iterations=10, seed=721)
    # nx.draw(graph, pos, **options)
    return graph


options = {
    "node_color": "black",
    "node_size": 2,
    "edge_color": "grey",
    "linewidths": 0,
    "width": 0.01,
}


############ API to Voltage ######################

import codecs, grpc, os
import lightning_pb2 as lnrpc, lightning_pb2_grpc as lightningstub

macaroon = codecs.encode(open("macaroon/admin.macaroon", "rb").read(), "hex")
os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
cert = open("tls/tls.cert", "rb").read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel(
    target="pulse.m.voltageapp.io:10009",
    credentials=ssl_creds,
    options=(
        ("grpc.max_send_message_length", 50 * 1024 * 1024),
        ("grpc.max_receive_message_length", 50 * 1024 * 1024),
    ),
)
stub = lightningstub.LightningStub(channel)
request = lnrpc.ChannelGraphRequest()
response = stub.DescribeGraph(request, metadata=[("macaroon", macaroon)])
print(response)
lngraph = json.loads(str(response))
############ Handling of received graph update ############


class ChannelGraphParser:
    def __init__(self, ChannelGraph):
        self.nodes = ChannelGraph.nodes
        self.edges = ChannelGraph.edges


class GraphNodes:
    def __init__(self, Nodes):
        self.last_update = Nodes.last_update
        self.pub_key = Nodes.pub_key
        self.alias = Nodes.alias
        self.color = Nodes.color


graph = ChannelGraphParser(response)

########### Plotting supporting functions


def get_graph(request):

    return graph
