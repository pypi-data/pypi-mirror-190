from enum import Enum
from opcua.ua import uaerrors
from pydevmgr_core import BaseNode
from .register import register 
from .uacom import UaComHandler, UAReadCollector, UAWriteCollector
from .uaengine import UaNodeEngine

from opcua import ua
from typing import Any
from pydantic import validator, Field
from systemy import autodoc

class UaNodeConfig(BaseNode.Config, UaNodeEngine.Config):
    type: str = 'Ua'
    attribute: ua.AttributeIds = Field( ua.AttributeIds.Value, description="OPC-UA Attribute specification")
    
    @validator("attribute", pre=True)
    def _validate_attribute(cls, value):
        if isinstance(value, str):
            return getattr(ua.AttributeIds, value)
        return value 


class RuntimNodeError(RuntimeError):
    """ Error handler, trying to get error more explicit """
    def __init__(self, err, node):
        complement = ""
        if isinstance( err , uaerrors.BadNodeIdUnknown ):
            complement = f"\n - Check if node id {node.engine.node_id} exists on server"
        if isinstance( err, AttributeError) and 'send_request' in str(err):
            complement = f"\n - check that connection to server has been established"
        msg =  f"({type(err).__name__}) {err} \n - When handling node {node!r}.{complement}"
        super().__init__(msg)



@register
@autodoc
class UaNode(BaseNode):
    """ Object representing a value node in opc-ua server

    This is an interface representing one single value (node) in an OPC-UA server. 
    
    
    Args:
        key (str, optional): Key description of the node 
        config (UeNode.Config, optional): as specified bellow  
        com (UaCom, UaEngine, optional): The communication protocol 
        **kwargs: config parameters as specified bellow


    __autodoc__ 

                    
    .. note::
            
                Several parser to ua Variant are defined in pydevmgr_ua and can be set with the `parser` argument: 
                
                - UaInt16, INT    (INT is an alias as TwinCat defines it)
                - UaInt32, DINT
                - UaInt64, LINT
                - UaUInt16, UINT
                - UaUInt32, UDINT
                - UaUInt64, ULINT
                - UaFloat, REAL
                - UaDouble, LREAL
                
                can also be created by VariantParser('Int16')                
                
    Example:
    
    In the example bellow it is assumed that the OPC UA server as a nodesid "ns=4;s=MAIN.Temp001" node
    defined.
    
    ::
    
        >>> from pydevmgr_ua import UaNode, UaCom
        >>> com = UaCom(address="opc.tcp://localhost:4840", namespace=4, prefix="MAIN")
        >>> temp = UaNode("temperature" , com=com, suffix="Temp001")
        >>> temp.get()
        
    Alternatively the com can be created on-the-fly
    

    One can build a UaInterface for several node 
    
    ::
    
        from pydevmgr_ua import UaInterface, UaNode, UaCom 
        from pydevmgr_core.nodes import Formula1
        
        class MyInterface(UaInterface):            
            temp_volt = UaNode.Config(suffix="Temp001")
            humidity = UaNode.Config(suffix="Humidity001")
            
            temp_kelvin = Formula1.Config(node="temp_volt", formula="230 + 1.234 * t", varname="t")
        
        com = UaCom(address= "opc.tcp://localhost:4840", namespace=4, prefix="MAIN")
        sensors = MyInterface('sensors', com=com)
        
    A UaDevice will create a com object from confurtion directly:

    ::

        from pydevmgr_ua import UaDevice, UaNode
        from pydevmgr_core.nodes import Formula1
        
        class MyDevice(UaDevice):            
            temp_volt = UaNode.Config(suffix="Temp001")
            humidity = UaNode.Config(suffix="Humidity001")
            
            temp_kelvin = Formula1.Config(node="temp_volt", formula="230 + 1.234 * t", varname="t")
        
        sensors = MyDevice( 'sensors', address="opc.tcp://localhost:4840", namespace=4, prefix="MAIN")


    """
    Config = UaNodeConfig
    Engine = UaNodeEngine
    
    com_handler = UaComHandler()

    @property
    def sid(self) -> Any:
        return self.com_handler.get_server_id( self.engine) 
    
    @property
    def uanodeid(self) -> ua.NodeId:
        return self.com_handler.get_nodeid( self.engine)
               
    def read_collector(self) -> UAReadCollector:
        """ Return a :class:`UAReadCollector` object to queue nodes for reading """
        return self.com_handler.read_collector(self.engine)
    
    def write_collector(self) -> UAWriteCollector:
        """ Return a :class:`UAWriteCollector` object to queue nodes and values for writing """
        return self.com_handler.write_collector(self.engine)
    
    def fget(self) -> Any:
        """ get the value from server """
        try:
            return self.com_handler.get_attribute( self.engine, self.config.attribute)
        except (RuntimeError, AttributeError) as e:
            raise RuntimNodeError(e, self)  from e 
           
    def fset(self, value: Any) -> None:
        """ set the value on server 
        
        Args:
            value (any): if :attr:`~UaNode.parser` is defined it is used to parse the value
                can be str, float, int, or :class:`ua.Variant` or  :class:`ua.DataValue` 
        """
        a = self.config.attribute
        datavalue = self._parse_value_for_ua(value) # is the node as a parser it as already been parsed
        try:
            self.com_handler.set_attribute( self.engine, a, datavalue)    
        except (RuntimeError, AttributeError) as e:
            raise RuntimNodeError(e, self)  from e 

            
    def _parse_value_for_ua(self, value: Any) -> None:
        return self.com_handler.parse_value(self.engine, value)
    
    def __repr__(self):
        type_ = type(self)
        # module = type_.__module__ 
        qualname = type_.__qualname__ 
        return f"<{qualname} key={self.key!r} <-> {self.engine.node_id} ({hex(id(self))})>"
