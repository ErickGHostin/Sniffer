import pyshark

def Captura(Onde):
    cap = pyshark.LiveCapture(interface=Onde)
    cap.sniff(packet_count=1)
    return cap