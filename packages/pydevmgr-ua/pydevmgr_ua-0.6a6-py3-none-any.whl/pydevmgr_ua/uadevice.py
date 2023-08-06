from pydevmgr_core import BaseDevice
from systemy  import autodoc
from .register import register
from .uacom import UaComHandler
from .uainterface import UaInterface
from .uanode import UaNode
from .uarpc import UaRpc
from .uaengine import UaEngine

@register
@autodoc
class UaDevice(BaseDevice):
    """ Represent a Device on an OPC-UA server 
    Args:
        
        key (optional, str): an optional key defining the device.
        config (optional, :UaInterface.Config): as defined bellow 
        com (optional, :class:`UaCom`, :class:`opcua.Client`, dict, str): 
            - if str create a :class:`UaCom` from the str address 
            - if :class:`opcua.Client` wrap it in a :class:`UaCom`
            - if :class:`UaCom` use it
        * *kwargs: configuration as defined bellow  

    __autodoc__ 
    """
    Node = UaNode
    Rpc = UaRpc
    Interface = UaInterface
    Engine = UaEngine
    com_handler = UaComHandler
    
    class Config(BaseDevice.Config, UaEngine.Config):
        Node = UaNode.Config
        Interface = UaInterface.Config
        Rpc = UaRpc.Config


    def connect(self):
        """ Connect to the OPC-UA client """
        return self.com_handler.connect(self.engine)
        
    def disconnect(self):
        """ Connect from the  OPC-UA client """
        return self.com_handler.disconnect(self.engine)
    
    def is_connected(self):
        return self.com_handler.is_connect(self.engine)
    
    
