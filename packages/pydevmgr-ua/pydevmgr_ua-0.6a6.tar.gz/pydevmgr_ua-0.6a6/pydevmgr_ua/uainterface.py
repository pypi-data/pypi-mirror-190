from pydevmgr_core import  BaseInterface
from systemy import autodoc 
from .register import register 
from .uacom import UaComHandler
from .uanode import UaNode
from .uaengine import UaEngine
from .uarpc import UaRpc

class UaInterfaceConfig(BaseInterface.Config, UaEngine.Config,  extra="allow"):
    Node = UaNode.Config
    Rpc = UaRpc.Config

    type: str = "Ua"
    prefix: str = "" # prefix added to com.prefix 
     
@register   
@autodoc
class UaInterface(BaseInterface):
    """ Interface OPC-UA communication    
    
    Args:
        
        key (optional, str): an optional key defining the interface.
        config (optional, :UaInterface.Config): as defined bellow 
        com (optional, :class:`UaCom`, :class:`opcua.Client`, dict, str): 
            - if str create a :class:`UaCom` from the str address 
            - if :class:`opcua.Client` wrap it in a :class:`UaCom`
            - if :class:`UaCom` use it
        * *kwargs: configuration as defined bellow  
        
    __autodoc__
      
    """
           
    Config = UaInterfaceConfig
    Engine = UaEngine
    Node = UaNode
    Rpc = UaRpc
    com_handler = UaComHandler() 

