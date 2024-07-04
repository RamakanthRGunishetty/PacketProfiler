import pyshark

def extract_features(pcap_path):
    """
    Extracts features from the pcap file located at pcap_path.
    :param pcap_path: Path to the pcap file
    :return: List of features extracted from the pcap file
    """
    features = []
    flows = {}

    capture = pyshark.FileCapture(pcap_path)

    for packet in capture:
        try:
            if 'IP' in packet and packet.transport_layer:
                protocol = 6 if packet.transport_layer == 'TCP' else 17
                src_port = int(packet[packet.transport_layer].srcport)
                dst_port = int(packet[packet.transport_layer].dstport)
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst

                flow_key = (src_ip, src_port, dst_ip, dst_port, protocol)

                if flow_key not in flows:
                    flows[flow_key] = {
                        'src2dst_packets': 0,
                        'src2dst_bytes': 0,
                        'dst2src_packets': 0,
                        'dst2src_bytes': 0
                    }

                flow = flows[flow_key]

                if packet.ip.src == src_ip:
                    flow['src2dst_packets'] += 1
                    flow['src2dst_bytes'] += int(packet.length)
                else:
                    flow['dst2src_packets'] += 1
                    flow['dst2src_bytes'] += int(packet.length)

        except AttributeError:
            # Skip packets that don't have the required attributes
            continue

    # Extract final feature values from the flows
    for flow_key, flow_value in flows.items():
        protocol, src_port, dst_port = flow_key[4], flow_key[1], flow_key[3]
        features.append([
            protocol,
            src_port,
            dst_port,
            flow_value['src2dst_packets'],
            flow_value['src2dst_bytes'],
            flow_value['dst2src_packets'],
            flow_value['dst2src_bytes']
        ])

    return features
