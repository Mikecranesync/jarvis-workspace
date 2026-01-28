"""Bridge to remote PLC client API."""
import os
import aiohttp
from typing import Optional, Dict, Any
from rivet_pro.infra.observability import get_logger

logger = get_logger(__name__)


class PLCBridge:
    """Async HTTP client for the remote PLC FastAPI backend."""

    def __init__(self, base_url: str = "http://localhost:9000/api"):
        self.base_url = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def connect(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)

    async def close(self):
        if self.session:
            await self.session.close()

    async def get_plc_status(self) -> Dict[str, Any]:
        try:
            async with self.session.get(f"{self.base_url}/plc/status") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"PLC status check failed: {e}")
            return {"error": str(e), "connected": False}

    async def read_io(self) -> Dict[str, Any]:
        try:
            async with self.session.get(f"{self.base_url}/plc/io") as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 503:
                    return {"error": "PLC not connected"}
                return {"error": f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"PLC I/O read failed: {e}")
            return {"error": str(e)}

    async def connect_plc(self, ip: str = "192.168.1.100", port: int = 502) -> Dict[str, Any]:
        try:
            async with self.session.post(
                f"{self.base_url}/plc/connect", json={"ip": ip, "port": port}
            ) as resp:
                return await resp.json()
        except Exception as e:
            logger.error(f"PLC connect failed: {e}")
            return {"error": str(e)}

    async def write_coil(self, address: int, value: bool) -> Dict[str, Any]:
        try:
            async with self.session.post(
                f"{self.base_url}/plc/write-coil",
                json={"address": address, "value": value},
            ) as resp:
                return await resp.json()
        except Exception as e:
            logger.error(f"PLC write failed: {e}")
            return {"error": str(e)}

    async def health_check(self) -> bool:
        try:
            async with self.session.get(f"{self.base_url}/health") as resp:
                return resp.status == 200
        except Exception:
            return False

    def format_io_for_telegram(self, io_data: Dict) -> str:
        if "error" in io_data:
            return f"PLC Error: {io_data['error']}"

        coils = io_data.get("coils", {})
        registers = io_data.get("registers", {})
        inputs = io_data.get("inputs", {})
        outputs = io_data.get("outputs", {})

        lines = ["<b>PLC Live Status</b>\n"]

        motor_status = "RUNNING" if coils.get("motor_running") else "STOPPED"
        conveyor_status = "RUNNING" if coils.get("conveyor_running") else "STOPPED"
        estop_status = "ENGAGED" if coils.get("e_stop_active") else "Clear"
        fault_status = "ACTIVE" if coils.get("fault_alarm") else "None"

        lines.append(f"<b>Motor:</b> {motor_status}")
        speed = registers.get("motor_speed")
        if speed:
            lines.append(f"  Speed: {speed}%")
        current = registers.get("motor_current")
        if current:
            lines.append(f"  Current: {current / 10:.1f}A")

        lines.append(f"<b>Conveyor:</b> {conveyor_status}")
        cspeed = registers.get("conveyor_speed")
        if cspeed:
            lines.append(f"  Speed: {cspeed}%")

        temp = registers.get("temperature", 0)
        lines.append(f"\n<b>Temperature:</b> {temp / 10:.1f}C")
        pressure = registers.get("pressure", 0)
        lines.append(f"<b>Pressure:</b> {pressure} PSI")

        lines.append(f"\n<b>E-Stop:</b> {estop_status}")
        lines.append(f"<b>Fault:</b> {fault_status}")

        s1 = "PART" if coils.get("sensor_1_active") else "clear"
        s2 = "PART" if coils.get("sensor_2_active") else "clear"
        lines.append(f"\n<b>Sensors:</b> S1={s1}, S2={s2}")

        if inputs:
            lines.append("\n<b>Inputs:</b>")
            for name, val in inputs.items():
                indicator = "ON" if val else "OFF"
                lines.append(f"  {indicator} {name}")

        if outputs:
            lines.append("\n<b>Outputs:</b>")
            for name, val in outputs.items():
                indicator = "ON" if val else "OFF"
                lines.append(f"  {indicator} {name}")

        ts = io_data.get("timestamp", "N/A")
        lines.append(f"\n{ts}")

        return "\n".join(lines)


PLC_BRIDGE_URL = os.environ.get("PLC_BRIDGE_URL", "http://localhost:9000/api")
plc_bridge = PLCBridge(base_url=PLC_BRIDGE_URL)
