#!/usr/bin/env python3
"""
Professional Mechanical Drawing Generator
Outputs DXF files with proper title blocks, dimensions, and annotations
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

def create_title_block(msp, doc, width, height, title, job_no, scale, drawn_by="JARVIS AI"):
    """Create professional title block"""
    # Main border
    msp.add_lwpolyline([(0, 0), (width, 0), (width, height), (0, height)], close=True)
    
    # Title block area (bottom right)
    tb_width = 4
    tb_height = 1.5
    tb_x = width - tb_width - 0.25
    tb_y = 0.25
    
    msp.add_lwpolyline([
        (tb_x, tb_y), 
        (tb_x + tb_width, tb_y), 
        (tb_x + tb_width, tb_y + tb_height), 
        (tb_x, tb_y + tb_height)
    ], close=True)
    
    # Title block text
    msp.add_text(title, height=0.15, dxfattribs={'style': 'STANDARD'}).set_placement(
        (tb_x + tb_width/2, tb_y + 1.2), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_text(f"JOB: {job_no}", height=0.1).set_placement(
        (tb_x + 0.1, tb_y + 0.9), align=TextEntityAlignment.LEFT)
    msp.add_text(f"SCALE: {scale}", height=0.1).set_placement(
        (tb_x + 0.1, tb_y + 0.6), align=TextEntityAlignment.LEFT)
    msp.add_text(f"DRAWN: {drawn_by}", height=0.1).set_placement(
        (tb_x + 0.1, tb_y + 0.3), align=TextEntityAlignment.LEFT)
    msp.add_text("FactoryLM", height=0.12, dxfattribs={'style': 'STANDARD'}).set_placement(
        (tb_x + tb_width/2, tb_y + 0.1), align=TextEntityAlignment.MIDDLE_CENTER)

def conveyor_side_view(msp, x, y, length=48, height=6, leg_height=30):
    """Draw conveyor side view"""
    # Frame rails
    msp.add_line((x, y + leg_height), (x + length, y + leg_height))  # Top rail
    msp.add_line((x, y + leg_height - 2), (x + length, y + leg_height - 2))  # Bottom rail
    
    # Legs
    for lx in [x + 4, x + length - 4]:
        msp.add_line((lx, y), (lx, y + leg_height))
        msp.add_line((lx + 2, y), (lx + 2, y + leg_height))
    
    # Drive roller (left)
    msp.add_circle((x + 4, y + leg_height - 1), radius=2)
    
    # Idler roller (right)
    msp.add_circle((x + length - 4, y + leg_height - 1), radius=1.5)
    
    # Belt line
    msp.add_line((x + 4, y + leg_height + 1), (x + length - 4, y + leg_height + 0.5))
    
    # Motor + Gearbox
    msp.add_lwpolyline([
        (x - 3, y + leg_height - 3),
        (x + 1, y + leg_height - 3),
        (x + 1, y + leg_height + 1),
        (x - 3, y + leg_height + 1)
    ], close=True)
    msp.add_text("MOTOR\n1HP", height=0.3).set_placement(
        (x - 1, y + leg_height - 1), align=TextEntityAlignment.MIDDLE_CENTER)

def add_dimensions(msp, doc):
    """Add dimension annotations"""
    dim_style = doc.dimstyles.get('STANDARD')
    
    # Overall length
    msp.add_linear_dim(base=(2, 36), p1=(2, 30), p2=(50, 30), 
                       dimstyle='STANDARD', override={'dimtxt': 0.2})

def create_conveyor_drawing(output_path='/tmp/conveyor_mechanical.dxf'):
    """Generate complete conveyor mechanical drawing"""
    doc = ezdxf.new('R2010')
    doc.units = units.IN  # Inches
    msp = doc.modelspace()
    
    # Drawing size (D-size: 34x22)
    WIDTH = 17
    HEIGHT = 11
    
    # Title block
    create_title_block(msp, doc, WIDTH, HEIGHT,
                      title="VFD CONVEYOR ASSEMBLY",
                      job_no="2026-0206-001",
                      scale="1:8")
    
    # Side view
    msp.add_text("SIDE VIEW", height=0.2).set_placement((2, 9), align=TextEntityAlignment.LEFT)
    conveyor_side_view(msp, x=2, y=2, length=12, height=2, leg_height=5)
    
    # Dimensions - length
    msp.add_text("48\"", height=0.15).set_placement((8, 1.5), align=TextEntityAlignment.MIDDLE_CENTER)
    msp.add_line((2, 1.7), (14, 1.7))  # Dimension line
    
    # Dimensions - height
    msp.add_text("36\"", height=0.15).set_placement((0.5, 4), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # Notes
    msp.add_text("NOTES:", height=0.12).set_placement((10, 9), align=TextEntityAlignment.LEFT)
    msp.add_text("1. MOTOR: 1HP, 56C, 1800RPM", height=0.08).set_placement((10, 8.7), align=TextEntityAlignment.LEFT)
    msp.add_text("2. GEARBOX: DORNER 32M020HS (20:1)", height=0.08).set_placement((10, 8.5), align=TextEntityAlignment.LEFT)
    msp.add_text("3. VFD: GS11N-20P2", height=0.08).set_placement((10, 8.3), align=TextEntityAlignment.LEFT)
    msp.add_text("4. OUTPUT SPEED: 90 RPM", height=0.08).set_placement((10, 8.1), align=TextEntityAlignment.LEFT)
    msp.add_text("5. FRAME: 2x4 LUMBER OR UNISTRUT", height=0.08).set_placement((10, 7.9), align=TextEntityAlignment.LEFT)
    
    doc.saveas(output_path)
    print(f"✅ Professional drawing saved: {output_path}")
    return output_path

if __name__ == '__main__':
    create_conveyor_drawing()
