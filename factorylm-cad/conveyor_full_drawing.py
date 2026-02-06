#!/usr/bin/env python3
"""
Complete Conveyor Mechanical Drawing Package
Generates all views needed for fabrication
"""
import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment
from datetime import datetime

class ConveyorDrawing:
    def __init__(self, job_no="2026-0206-001", 
                 length=48, width=14, height=36,
                 motor_hp=1, gear_ratio=20, output_rpm=90):
        self.job_no = job_no
        self.length = length
        self.width = width  
        self.height = height
        self.motor_hp = motor_hp
        self.gear_ratio = gear_ratio
        self.output_rpm = output_rpm
        self.doc = ezdxf.new('R2010')
        self.doc.units = units.IN
        self.msp = self.doc.modelspace()
        
    def title_block(self, x, y, title, sheet="1 OF 3"):
        """Professional title block"""
        w, h = 4, 2
        
        # Border
        self.msp.add_lwpolyline([
            (x, y), (x+w, y), (x+w, y+h), (x, y+h)
        ], close=True, dxfattribs={'lineweight': 50})
        
        # Divider lines
        self.msp.add_line((x, y+1.4), (x+w, y+1.4))
        self.msp.add_line((x, y+0.7), (x+w, y+0.7))
        self.msp.add_line((x+2, y), (x+2, y+0.7))
        
        # Text
        self.msp.add_text("FactoryLM", height=0.2, 
            dxfattribs={'style': 'STANDARD'}).set_placement(
            (x+w/2, y+1.7), align=TextEntityAlignment.MIDDLE_CENTER)
        self.msp.add_text(title, height=0.15).set_placement(
            (x+w/2, y+1.1), align=TextEntityAlignment.MIDDLE_CENTER)
        self.msp.add_text(f"JOB: {self.job_no}", height=0.1).set_placement(
            (x+0.1, y+0.5), align=TextEntityAlignment.LEFT)
        self.msp.add_text(f"DATE: {datetime.now().strftime('%Y-%m-%d')}", height=0.1).set_placement(
            (x+0.1, y+0.3), align=TextEntityAlignment.LEFT)
        self.msp.add_text(f"SCALE: NTS", height=0.1).set_placement(
            (x+0.1, y+0.1), align=TextEntityAlignment.LEFT)
        self.msp.add_text(f"SHEET: {sheet}", height=0.1).set_placement(
            (x+2.1, y+0.5), align=TextEntityAlignment.LEFT)
        self.msp.add_text("DRAWN: JARVIS AI", height=0.1).set_placement(
            (x+2.1, y+0.3), align=TextEntityAlignment.LEFT)

    def drawing_border(self, w=17, h=11):
        """Standard D-size border"""
        # Outer border
        self.msp.add_lwpolyline([
            (0, 0), (w, 0), (w, h), (0, h)
        ], close=True, dxfattribs={'lineweight': 70})
        # Inner border
        margin = 0.25
        self.msp.add_lwpolyline([
            (margin, margin), (w-margin, margin), 
            (w-margin, h-margin), (margin, h-margin)
        ], close=True, dxfattribs={'lineweight': 35})

    def side_view(self, x, y, scale=0.15):
        """Side elevation view"""
        L = self.length * scale
        H = self.height * scale
        leg_w = 2 * scale
        roller_r = 3 * scale
        
        # Label
        self.msp.add_text("SIDE VIEW", height=0.2).set_placement(
            (x + L/2, y + H + 1), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Frame top rail
        self.msp.add_line((x, y + H), (x + L, y + H))
        self.msp.add_line((x, y + H - 0.3), (x + L, y + H - 0.3))
        
        # Legs
        for lx in [x + 3*scale, x + L - 3*scale]:
            self.msp.add_lwpolyline([
                (lx, y), (lx + leg_w, y), 
                (lx + leg_w, y + H), (lx, y + H)
            ], close=True)
        
        # Drive roller (left)
        self.msp.add_circle((x + 4*scale, y + H - roller_r/2), radius=roller_r)
        self.msp.add_text("DRIVE", height=0.1).set_placement(
            (x + 4*scale, y + H - roller_r - 0.3), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Idler roller (right)  
        self.msp.add_circle((x + L - 4*scale, y + H - roller_r/2), radius=roller_r*0.7)
        self.msp.add_text("IDLER", height=0.1).set_placement(
            (x + L - 4*scale, y + H - roller_r - 0.3), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Motor + Gearbox
        motor_w = 4 * scale
        motor_h = 3 * scale
        self.msp.add_lwpolyline([
            (x - motor_w, y + H - motor_h),
            (x, y + H - motor_h),
            (x, y + H + motor_h/2),
            (x - motor_w, y + H + motor_h/2)
        ], close=True)
        self.msp.add_text(f"MOTOR\n{self.motor_hp}HP", height=0.12).set_placement(
            (x - motor_w/2, y + H - motor_h/4), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Gearbox
        gb_w = 2 * scale
        self.msp.add_lwpolyline([
            (x, y + H - motor_h/2),
            (x + gb_w, y + H - motor_h/2),
            (x + gb_w, y + H + motor_h/4),
            (x, y + H + motor_h/4)
        ], close=True)
        self.msp.add_text(f"{self.gear_ratio}:1", height=0.1).set_placement(
            (x + gb_w/2, y + H - motor_h/4), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Dimensions
        self.msp.add_text(f'{self.length}"', height=0.12).set_placement(
            (x + L/2, y - 0.4), align=TextEntityAlignment.MIDDLE_CENTER)
        self.msp.add_line((x, y - 0.2), (x + L, y - 0.2))
        self.msp.add_line((x, y - 0.1), (x, y - 0.3))
        self.msp.add_line((x + L, y - 0.1), (x + L, y - 0.3))
        
        self.msp.add_text(f'{self.height}"', height=0.12).set_placement(
            (x - motor_w - 0.5, y + H/2), align=TextEntityAlignment.MIDDLE_CENTER)
        
    def top_view(self, x, y, scale=0.15):
        """Top/plan view"""
        L = self.length * scale
        W = self.width * scale
        
        self.msp.add_text("TOP VIEW", height=0.2).set_placement(
            (x + L/2, y + W + 0.5), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Frame outline
        self.msp.add_lwpolyline([
            (x, y), (x + L, y), (x + L, y + W), (x, y + W)
        ], close=True)
        
        # Belt area (dashed)
        belt_margin = 1 * scale
        self.msp.add_lwpolyline([
            (x + belt_margin, y + belt_margin),
            (x + L - belt_margin, y + belt_margin),
            (x + L - belt_margin, y + W - belt_margin),
            (x + belt_margin, y + W - belt_margin)
        ], close=True, dxfattribs={'linetype': 'DASHED'})
        self.msp.add_text("BELT", height=0.1).set_placement(
            (x + L/2, y + W/2), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Dimension
        self.msp.add_text(f'{self.width}"', height=0.12).set_placement(
            (x - 0.5, y + W/2), align=TextEntityAlignment.MIDDLE_CENTER)

    def end_view(self, x, y, scale=0.15):
        """End elevation view"""
        W = self.width * scale
        H = self.height * scale
        
        self.msp.add_text("END VIEW", height=0.2).set_placement(
            (x + W/2, y + H + 0.5), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Frame
        self.msp.add_lwpolyline([
            (x, y), (x + W, y), (x + W, y + H), (x, y + H)
        ], close=True)
        
        # Legs
        leg_w = 2 * scale
        for lx in [x + scale, x + W - scale - leg_w]:
            self.msp.add_lwpolyline([
                (lx, y), (lx + leg_w, y),
                (lx + leg_w, y + H - 0.5), (lx, y + H - 0.5)
            ], close=True)
        
        # Roller (circle)
        self.msp.add_circle((x + W/2, y + H - 0.3), radius=2*scale)

    def bom_table(self, x, y):
        """Bill of Materials"""
        self.msp.add_text("BILL OF MATERIALS", height=0.15).set_placement(
            (x, y), align=TextEntityAlignment.LEFT)
        
        bom = [
            ("1", "Motor", f"{self.motor_hp}HP 56C 3PH 1800RPM", "1"),
            ("2", "Gearbox", f"Dorner 32M020HS ({self.gear_ratio}:1)", "1"),
            ("3", "VFD", "GS11N-20P2", "1"),
            ("4", "Frame Rail", f'2x4 Lumber {self.length}"', "2"),
            ("5", "Cross Brace", f'2x4 Lumber {self.width}"', "4"),
            ("6", "Legs", '2x4 Lumber 36"', "4"),
            ("7", "Drive Roller", '1.5" PVC x 14"', "1"),
            ("8", "Idler Roller", '1.5" PVC x 14"', "1"),
            ("9", "Belt", f'Rubber Mat {self.length}" x {self.width}"', "1"),
            ("10", "Hardware", "Screws, bolts, brackets", "LOT"),
        ]
        
        row_h = 0.18
        for i, (item, desc, spec, qty) in enumerate(bom):
            yy = y - 0.3 - (i * row_h)
            self.msp.add_text(item, height=0.08).set_placement((x, yy), align=TextEntityAlignment.LEFT)
            self.msp.add_text(desc, height=0.08).set_placement((x+0.4, yy), align=TextEntityAlignment.LEFT)
            self.msp.add_text(spec, height=0.08).set_placement((x+1.5, yy), align=TextEntityAlignment.LEFT)
            self.msp.add_text(qty, height=0.08).set_placement((x+4.2, yy), align=TextEntityAlignment.LEFT)

    def notes(self, x, y):
        """Construction notes"""
        self.msp.add_text("NOTES:", height=0.12).set_placement((x, y), align=TextEntityAlignment.LEFT)
        
        notes = [
            f"1. MOTOR: {self.motor_hp}HP, 56C FRAME, 1800RPM, 3-PHASE",
            f"2. GEARBOX: DORNER 32M020HS, {self.gear_ratio}:1 RATIO",
            f"3. OUTPUT SPEED: {self.output_rpm} RPM",
            "4. VFD: AUTOMATIONDIRECT GS11N-20P2",
            "5. FRAME: 2x4 LUMBER OR UNISTRUT",
            "6. BELT: RUBBER MAT OR PVC CONVEYOR BELT",
            "7. ALL DIMENSIONS IN INCHES",
            "8. WORKING HEIGHT: 36\" (ERGONOMIC)",
        ]
        
        for i, note in enumerate(notes):
            self.msp.add_text(note, height=0.08).set_placement(
                (x, y - 0.2 - (i * 0.15)), align=TextEntityAlignment.LEFT)

    def generate_full_drawing(self, output_path):
        """Generate complete multi-view drawing"""
        # Border
        self.drawing_border(17, 11)
        
        # Title block
        self.title_block(12.5, 0.3, "VFD CONVEYOR ASSEMBLY", "1 OF 1")
        
        # Views
        self.side_view(1, 1.5, scale=0.12)
        self.top_view(1, 7, scale=0.12)
        self.end_view(10, 7, scale=0.15)
        
        # BOM
        self.bom_table(10, 5.5)
        
        # Notes
        self.notes(10, 3)
        
        # Save
        self.doc.saveas(output_path)
        print(f"✅ Complete drawing saved: {output_path}")
        return output_path


def generate_conveyor_package(job_no="2026-0206-001", output_dir="/tmp"):
    """Generate complete drawing package"""
    drawing = ConveyorDrawing(
        job_no=job_no,
        length=48,
        width=14, 
        height=36,
        motor_hp=1,
        gear_ratio=20,
        output_rpm=90
    )
    
    dxf_path = f"{output_dir}/conveyor_complete_{job_no}.dxf"
    drawing.generate_full_drawing(dxf_path)
    
    return dxf_path


if __name__ == '__main__':
    generate_conveyor_package()
