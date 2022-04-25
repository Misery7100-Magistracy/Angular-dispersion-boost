from .utils import configure_mpl
from .mph import Engine as MphEngine
from .mph import Field2D as Field2DEngine
from .matlab import Engine as MatlabEngine
from .matlab import MSTM as MstmEngine
from .lpic import Engine as LpicEngine
from .mesh import MeshGenerator
from .eqs import resonance_m_squared

default_palette = [
        
        '#4078c0', 
        '#6cc644',
        '#bd2c00',
        '#c9510c',
        '#6e5494'
    
    ]