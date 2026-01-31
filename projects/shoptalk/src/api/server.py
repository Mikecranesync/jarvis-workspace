#!/usr/bin/env python3
"""
ShopTalk API Server
REST and WebSocket API for equipment monitoring.
"""

import asyncio
import json
import time
import logging
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")

from model.world_model import WorldModel, EquipmentState, create_conveyor_model
from inference.engine import InferenceEngine, SimulatedDataSource, InferenceResult
from voice.tts import VoiceInterface, DiagnosticAnnouncer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ShopTalkAPI")

# Create FastAPI app
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="ShopTalk Edge AI",
        description="Industrial equipment diagnostics API",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app = None

# Global state
model: Optional[WorldModel] = None
engine: Optional[InferenceEngine] = None
voice: Optional[VoiceInterface] = None
announcer: Optional[DiagnosticAnnouncer] = None
websocket_clients: List[WebSocket] = []


# Pydantic models
class StatusResponse(BaseModel):
    status: str
    model_trained: bool
    total_samples: int
    total_anomalies: int
    language: str


class DiagnosisRequest(BaseModel):
    sensors: Dict[str, float]
    controls: Optional[Dict[str, float]] = {}
    discrete: Optional[Dict[str, bool]] = {}


class DiagnosisResponse(BaseModel):
    is_anomaly: bool
    anomalies: List[Dict]
    diagnosis: str
    prediction: Dict[str, float]
    z_scores: Dict[str, float]


class LanguageRequest(BaseModel):
    language: str


class ScenarioRequest(BaseModel):
    scenario: str  # normal, jam, overload, bearing_failure


# API Routes
if FASTAPI_AVAILABLE:
    
    @app.get("/")
    async def root():
        """API root."""
        return {
            "name": "ShopTalk Edge AI",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs"
        }
    
    @app.get("/status", response_model=StatusResponse)
    async def get_status():
        """Get system status."""
        stats = engine.get_stats() if engine else {}
        return StatusResponse(
            status="running" if engine and engine.running else "idle",
            model_trained=model.is_trained if model else False,
            total_samples=stats.get("total_samples", 0),
            total_anomalies=stats.get("total_anomalies", 0),
            language=voice.language if voice else "en"
        )
    
    @app.post("/diagnose", response_model=DiagnosisResponse)
    async def diagnose(request: DiagnosisRequest):
        """Run diagnosis on provided sensor data."""
        if not model or not model.is_trained:
            raise HTTPException(status_code=503, detail="Model not trained")
        
        # Create state from request
        state = EquipmentState(
            timestamp=time.time(),
            sensors=request.sensors,
            controls=request.controls or {},
            discrete=request.discrete or {}
        )
        
        # Run through model
        result = model.update(state)
        
        diagnosis = ""
        if result.get("is_anomaly"):
            diagnosis = model.diagnose(result.get("anomalies", []))
            
            # Announce if enabled
            if announcer:
                announcer.announce(diagnosis, result.get("anomalies", []))
        
        return DiagnosisResponse(
            is_anomaly=result.get("is_anomaly", False),
            anomalies=result.get("anomalies", []),
            diagnosis=diagnosis,
            prediction=result.get("prediction", {}),
            z_scores=result.get("z_scores", {})
        )
    
    @app.post("/language")
    async def set_language(request: LanguageRequest):
        """Set voice language."""
        if voice:
            voice.set_language(request.language)
        return {"language": request.language}
    
    @app.post("/speak")
    async def speak(text: str):
        """Speak text using TTS."""
        if voice:
            output = voice.speak(text, play=False)
            if output:
                return FileResponse(output, media_type="audio/mpeg")
        raise HTTPException(status_code=503, detail="TTS not available")
    
    @app.post("/scenario")
    async def set_scenario(request: ScenarioRequest):
        """Set simulation scenario (for demo mode)."""
        if hasattr(engine, 'data_source') and hasattr(engine.data_source, 'set_scenario'):
            engine.data_source.set_scenario(request.scenario)
            return {"scenario": request.scenario}
        raise HTTPException(status_code=400, detail="Not in simulation mode")
    
    @app.get("/model/stats")
    async def model_stats():
        """Get model statistics."""
        if not model:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        return {
            "features": model.feature_order,
            "trained": model.is_trained,
            "training_samples": model.training_samples,
            "means": model.means.tolist() if model.means is not None else None,
            "stds": model.stds.tolist() if model.stds is not None else None
        }
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket for real-time updates."""
        await websocket.accept()
        websocket_clients.append(websocket)
        logger.info(f"WebSocket client connected. Total: {len(websocket_clients)}")
        
        try:
            while True:
                # Keep connection alive and handle incoming messages
                data = await websocket.receive_text()
                
                # Handle commands
                try:
                    cmd = json.loads(data)
                    if cmd.get("type") == "ping":
                        await websocket.send_json({"type": "pong"})
                    elif cmd.get("type") == "set_language":
                        if voice:
                            voice.set_language(cmd.get("language", "en"))
                            await websocket.send_json({
                                "type": "language_set",
                                "language": voice.language
                            })
                except json.JSONDecodeError:
                    pass
                    
        except WebSocketDisconnect:
            websocket_clients.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total: {len(websocket_clients)}")


async def broadcast_result(result: InferenceResult):
    """Broadcast inference result to all WebSocket clients."""
    if not websocket_clients:
        return
    
    message = {
        "type": "inference",
        "timestamp": result.timestamp,
        "is_anomaly": result.is_anomaly,
        "anomalies": result.anomalies,
        "diagnosis": result.diagnosis,
        "prediction": result.prediction,
        "z_scores": result.z_scores,
        "raw_state": result.raw_state
    }
    
    for client in websocket_clients[:]:  # Copy list to avoid modification during iteration
        try:
            await client.send_json(message)
        except (WebSocketDisconnect, ConnectionError, RuntimeError) as e:
            logger.debug(f"Removing disconnected client: {e}")
            websocket_clients.remove(client)


def setup_engine(simulate: bool = True, scenario: str = "normal",
                 host: str = "192.168.1.100", port: int = 502,
                 language: str = "en"):
    """Setup the inference engine."""
    global model, engine, voice, announcer
    
    # Create model
    model = create_conveyor_model()
    
    # Create engine
    engine = InferenceEngine(model, sample_interval=0.1)
    
    # Setup data source
    if simulate:
        source = SimulatedDataSource(scenario)
        engine.set_data_source(source)
        logger.info(f"Using simulated data source: {scenario}")
    else:
        from inference.engine import create_modbus_data_source
        source = create_modbus_data_source(host, port)
        if source:
            engine.set_data_source(source)
            logger.info(f"Connected to PLC at {host}:{port}")
        else:
            source = SimulatedDataSource(scenario)
            engine.set_data_source(source)
            logger.warning("Falling back to simulation")
    
    # Train model on initial data
    logger.info("Training model on initial samples...")
    training_data = []
    for i in range(100):
        data = source()
        state = EquipmentState(
            timestamp=float(i),
            sensors={k: v for k, v in data.items() if isinstance(v, (int, float))},
            controls={},
            discrete={k: v for k, v in data.items() if isinstance(v, bool)}
        )
        training_data.append(state)
    model.train(training_data)
    logger.info("Training complete")
    
    # Setup voice
    voice = VoiceInterface(language=language)
    announcer = DiagnosticAnnouncer(voice, cooldown=30.0)
    
    # Setup callbacks
    def on_update(result: InferenceResult):
        # Broadcast to WebSocket clients
        asyncio.create_task(broadcast_result(result))
    
    def on_anomaly(result: InferenceResult):
        logger.warning(f"Anomaly: {result.diagnosis}")
        if announcer:
            announcer.announce(result.diagnosis, result.anomalies)
    
    engine.set_on_update(on_update)
    engine.set_on_anomaly(on_anomaly)


async def run_engine():
    """Run inference engine in background."""
    if engine:
        await engine.run_async()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="ShopTalk API Server")
    parser.add_argument("--host", default="0.0.0.0", help="API host")
    parser.add_argument("--port", type=int, default=8080, help="API port")
    parser.add_argument("--simulate", action="store_true", help="Use simulated data")
    parser.add_argument("--scenario", default="normal", help="Simulation scenario")
    parser.add_argument("--plc-host", default="192.168.1.100", help="PLC IP")
    parser.add_argument("--plc-port", type=int, default=502, help="Modbus port")
    parser.add_argument("--language", default="en", help="Voice language")
    args = parser.parse_args()
    
    if not FASTAPI_AVAILABLE:
        print("Error: FastAPI not installed")
        return
    
    # Setup
    setup_engine(
        simulate=args.simulate,
        scenario=args.scenario,
        host=args.plc_host,
        port=args.plc_port,
        language=args.language
    )
    
    # Run
    logger.info(f"Starting ShopTalk API on http://{args.host}:{args.port}")
    
    # Start inference in background
    @app.on_event("startup")
    async def startup_event():
        asyncio.create_task(run_engine())
    
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
