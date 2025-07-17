"""
UltraRF Feature Test
Test adaptive modem, channel bonding, LDPC, QoS, mesh services, and station ID.
"""
import numpy as np
from src.physical.adaptive_modem import AdaptiveModem
from src.physical.channel_bonding import ChannelBonding
from src.physical.ldpc_codec import LDPCCodec
from src.mac.qos_manager import QoSManager
from src.network.mesh_services import MeshServices
from src.mac.station_id import StationID
import time

def test_adaptive_modem():
    modem = AdaptiveModem()
    assert modem.select_mcs(3) == 'QPSK'
    assert modem.select_mcs(15) == '16QAM'
    assert modem.select_mcs(30) == '256QAM'

def test_channel_bonding():
    bonding = ChannelBonding([0,1,2])
    data = np.arange(9)
    split = bonding.aggregate(data)
    assert all(len(x) == 3 for x in split)
    combined = bonding.combine(split)
    assert np.allclose(combined, data)

def test_ldpc_codec():
    codec = LDPCCodec()
    bits = np.array([1,0,1,1,0])
    codeword = codec.encode(bits)
    decoded = codec.decode(codeword)
    assert np.allclose(bits, decoded)

def test_qos_manager():
    qos = QoSManager()
    assert qos.get_guarantee(0) == 1.0
    assert qos.get_guarantee(1) == 0.8
    assert qos.get_guarantee(2) == 0.6
    assert qos.get_guarantee(3) == 0.0

def test_mesh_services():
    mesh = MeshServices()
    mesh.add_path('X', ['A','B'])
    mesh.add_path('X', ['C','D'])
    assert mesh.get_primary('X') == ['A','B']
    assert mesh.get_backups('X') == [['C','D']]
    assert mesh.load_balance('X') == ['A','B']
    assert mesh.load_balance('X') == ['C','D']

def test_station_id():
    sid = StationID('N0CALL')
    sid.last_sent = time.time() - 601
    assert sid.should_send() is True
    assert sid.get_id_frame() == b'N0CALL'
    assert sid.should_send() is False

if __name__ == '__main__':
    test_adaptive_modem()
    test_channel_bonding()
    test_ldpc_codec()
    test_qos_manager()
    test_mesh_services()
    test_station_id()
    print('All feature tests passed.')
