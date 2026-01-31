#!/usr/bin/env python3
"""
Spanish Language Training Data for ShopTalk
Bilingual samples for Latin American industrial workforce.
"""

import json
import random
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent

# Spanish equipment and fault vocabulary
SPANISH_TEMPLATES = {
    "conveyor": {
        "name": "transportador de banda",
        "faults": {
            "jam": {
                "diagnosis": "Atasco de Banda Detectado",
                "explanation": "Corriente del motor alta con velocidad de banda baja indica obstrucción mecánica.",
                "actions": [
                    "PARE el transportador inmediatamente usando el paro de emergencia",
                    "Siga el procedimiento de bloqueo/etiquetado antes de acercarse",
                    "Inspeccione la banda buscando acumulación de producto o escombros",
                    "Revise si hay objetos atrapados en los rodillos o poleas",
                    "Retire cualquier obstrucción encontrada",
                    "Verifique la tensión y alineación de la banda",
                    "Pruebe a baja velocidad antes de reanudar operación completa"
                ]
            },
            "overload": {
                "diagnosis": "Condición de Sobrecarga del Motor",
                "explanation": "Consumo de corriente elevado y temperatura en aumento sugieren que el motor está trabajando más de lo diseñado.",
                "actions": [
                    "Reduzca la carga en el transportador si es posible",
                    "Revise si hay acumulación de producto o carga desigual",
                    "Inspeccione el funcionamiento del ventilador de enfriamiento",
                    "Verifique que la tensión de la banda no esté muy apretada",
                    "Revise los rodamientos buscando señales de desgaste",
                    "Monitoree la temperatura - apague si excede 70°C"
                ]
            },
            "bearing": {
                "diagnosis": "Posible Falla de Rodamiento",
                "explanation": "Temperatura alta con corriente normal sugiere fricción por rodamientos desgastados.",
                "actions": [
                    "Programe inspección inmediata de rodamientos",
                    "Revise los niveles de lubricación en todos los rodamientos",
                    "Escuche si hay sonidos inusuales de rechinido o chirrido",
                    "Monitoree la vibración si hay sensor disponible",
                    "Planee reemplazo de rodamientos en próxima ventana de mantenimiento",
                    "Reduzca la velocidad para extender vida del rodamiento hasta el reemplazo"
                ]
            }
        }
    },
    "pump": {
        "name": "bomba",
        "faults": {
            "cavitation": {
                "diagnosis": "Cavitación Detectada",
                "explanation": "Bajo flujo con baja presión de entrada indica la bomba está cavitando.",
                "actions": [
                    "Revise el nivel del tanque de succión",
                    "Inspeccione el filtro de succión buscando bloqueo",
                    "Verifique que la válvula de succión esté completamente abierta",
                    "Revise si hay fugas de aire en la línea de succión",
                    "Confirme que la bomba esté correctamente cebada"
                ]
            },
            "seal_leak": {
                "diagnosis": "Fuga de Sello Mecánico",
                "explanation": "Pérdida de líquido visible cerca del eje de la bomba.",
                "actions": [
                    "Detenga la bomba de forma segura",
                    "Evalúe la tasa de fuga",
                    "Programe reemplazo de sello",
                    "Revise alineación del eje",
                    "Inspeccione las caras del sello buscando daño"
                ]
            }
        }
    },
    "motor": {
        "name": "motor",
        "faults": {
            "phase_imbalance": {
                "diagnosis": "Desbalance de Fase Detectado",
                "explanation": "Una fase consume significativamente más corriente que las otras.",
                "actions": [
                    "Revise todas las conexiones de fase en terminales del motor",
                    "Mida el voltaje en cada fase",
                    "Inspeccione los contactos del contactor buscando picaduras",
                    "Realice prueba de megger en los devanados del motor"
                ]
            },
            "overheating": {
                "diagnosis": "Sobrecalentamiento del Motor",
                "explanation": "Motor sobrecalentando con consumo de corriente elevado.",
                "actions": [
                    "Reduzca la carga inmediatamente",
                    "Revise el funcionamiento del ventilador de enfriamiento",
                    "Limpie las aletas y ventilaciones del motor",
                    "Verifique que el motor esté correctamente dimensionado para la aplicación"
                ]
            }
        }
    }
}


def generate_spanish_sample(equipment: str, fault: str) -> dict:
    """Generate a Spanish language training sample."""
    config = SPANISH_TEMPLATES[equipment]
    fault_config = config["faults"][fault]
    
    # Generate realistic readings
    readings = {
        "corriente_motor": f"{random.uniform(6, 10):.1f} A",
        "velocidad_motor": f"{random.randint(800, 1200)} RPM",
        "temperatura": f"{random.uniform(55, 72):.1f}°C",
        "velocidad_banda": f"{random.randint(20, 50)}%"
    }
    
    readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
    actions_str = "\n".join([f"{i+1}. {a}" for i, a in enumerate(fault_config["actions"])])
    
    instruction = f"El {config['name']} tiene una alarma. Lecturas: {readings_str}. ¿Cuál es el problema?"
    
    output = f"""**Diagnóstico: {fault_config['diagnosis']}**

{fault_config['explanation']}

**Lecturas Anormales:**
""" + "\n".join([f"- {k}: {v}" for k, v in readings.items()]) + f"""

**Acciones Recomendadas:**
{actions_str}

**Nota de Seguridad:** Siempre siga los procedimientos de bloqueo/etiquetado antes de cualquier inspección o mantenimiento."""
    
    return {
        "instruction": instruction,
        "input": f"Equipo: {config['name'].title()}",
        "output": output,
        "language": "es",
        "equipment": equipment,
        "fault": fault
    }


def generate_spanish_normal_sample(equipment: str) -> dict:
    """Generate a Spanish normal operation sample."""
    config = SPANISH_TEMPLATES[equipment]
    
    readings = {
        "corriente_motor": f"{random.uniform(4, 5.5):.1f} A",
        "velocidad_motor": f"{random.randint(1450, 1550)} RPM",
        "temperatura": f"{random.uniform(42, 52):.1f}°C"
    }
    
    readings_str = ", ".join([f"{k}: {v}" for k, v in readings.items()])
    
    return {
        "instruction": f"Revise el estado del {config['name']}. Lecturas: {readings_str}",
        "input": "",
        "output": f"El {config['name']} está operando normalmente.\n\n**Lecturas Actuales:**\n" + 
                  "\n".join([f"- {k}: {v} ✓" for k, v in readings.items()]) +
                  "\n\n✅ Todos los parámetros dentro del rango normal. No se requiere acción.",
        "language": "es",
        "equipment": equipment,
        "fault": "normal"
    }


def generate_spanish_dataset(n_per_fault: int = 30) -> list:
    """Generate Spanish training dataset."""
    dataset = []
    
    for equipment, config in SPANISH_TEMPLATES.items():
        print(f"Generating Spanish samples for: {equipment}")
        
        # Normal samples
        for _ in range(n_per_fault):
            dataset.append(generate_spanish_normal_sample(equipment))
        
        # Fault samples
        for fault in config["faults"].keys():
            for _ in range(n_per_fault):
                dataset.append(generate_spanish_sample(equipment, fault))
    
    return dataset


if __name__ == "__main__":
    print("Generating Spanish Training Data...")
    
    dataset = generate_spanish_dataset(n_per_fault=40)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"spanish_train_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([{"instruction": d["instruction"], "input": d["input"], "output": d["output"]} 
                   for d in dataset], f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(dataset)} Spanish samples → {output_file}")
