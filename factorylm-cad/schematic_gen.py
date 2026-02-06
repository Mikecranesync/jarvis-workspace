#!/usr/bin/env python3
"""Generate electrical schematics"""
import schemdraw
import schemdraw.elements as elm

def vfd_motor_schematic(output_path='/tmp/vfd_motor_schematic.svg'):
    """Generate VFD to Motor wiring schematic"""
    d = schemdraw.Drawing()
    d.config(unit=3, fontsize=10)
    
    # Power source
    d += elm.Line().right().length(1).label('L1', 'left')
    d += elm.Dot()
    d += elm.Line().right().length(3).label('220V Input')
    d += elm.Dot()
    
    # VFD box (using resistor box as placeholder)
    d += elm.RBox().right().label('VFD\nGS11N-20P2')
    
    # Output to motor
    d += elm.Line().right().length(2).label('U,V,W')
    d += elm.Motor().label('M\n1HP 56C', 'bottom')
    
    d.save(output_path)
    print(f"✅ Saved: {output_path}")
    return output_path

if __name__ == '__main__':
    vfd_motor_schematic()
