interface IOTableProps {
  coils: Record<string, boolean> | null
  inputs: Record<string, boolean> | null
  outputs: Record<string, boolean> | null
  registers: Record<string, number> | null
  onToggleCoil: (address: number, value: boolean, name: string) => void
}

// Micro820 I/O descriptions
const INPUT_DESCRIPTIONS: Record<string, string> = {
  DI_00: '3-Pos Switch CENTER',
  DI_01: 'E-Stop NO Contact',
  DI_02: 'E-Stop NC Contact',
  DI_03: '3-Pos Switch RIGHT',
  DI_04: 'Left Pushbutton',
  DI_05: 'Right Pushbutton',
  DI_06: 'Spare Input 6',
  DI_07: 'Spare Input 7',
  DI_08: 'Spare Input 8',
  DI_09: 'Spare Input 9',
  DI_10: 'Spare Input 10',
  DI_11: 'Spare Input 11',
}

const OUTPUT_DESCRIPTIONS: Record<string, string> = {
  DO_00: 'Indicator Light 1',
  DO_01: 'Indicator Light 2',
  DO_02: 'Indicator Light 3',
  DO_03: 'Indicator Light 4',
  DO_04: 'Relay Output 1',
  DO_05: 'Relay Output 2',
  DO_06: 'Relay Output 3',
}

// Map output names to coil addresses for write operations
const OUTPUT_ADDRESSES: Record<string, number> = {
  DO_00: 15,
  DO_01: 16,
  DO_02: 17,
  DO_03: 18,
  DO_04: 19,
  DO_05: 20,
  DO_06: 21,
}

function BoolIndicator({ 
  value, 
  onClick, 
  clickable = false 
}: { 
  value: boolean
  onClick?: () => void
  clickable?: boolean 
}) {
  return (
    <button
      onClick={onClick}
      disabled={!clickable}
      className={`w-16 py-1 rounded text-sm font-medium transition-all ${
        value
          ? 'bg-green-500 text-white shadow-lg shadow-green-500/30'
          : 'bg-gray-300 text-gray-600'
      } ${clickable ? 'hover:scale-105 cursor-pointer' : 'cursor-default'}`}
    >
      {value ? 'ON' : 'OFF'}
    </button>
  )
}

function IOTable({ coils, inputs, outputs, registers, onToggleCoil }: IOTableProps) {
  if (!inputs && !outputs) {
    return (
      <div className="text-center py-8 text-gray-500">
        <div className="animate-pulse">Loading I/O data...</div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Physical Inputs */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <h3 className="text-lg font-semibold p-4 border-b bg-blue-50 text-blue-800">
          📥 Digital Inputs
        </h3>
        <div className="divide-y">
          {inputs && Object.entries(inputs).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between px-4 py-3 hover:bg-gray-50">
              <div>
                <span className="font-medium">{key}</span>
                <span className="text-gray-500 text-sm ml-2">
                  {INPUT_DESCRIPTIONS[key] || ''}
                </span>
              </div>
              <BoolIndicator value={value} />
            </div>
          ))}
        </div>
      </div>

      {/* Physical Outputs - CONTROLLABLE */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <h3 className="text-lg font-semibold p-4 border-b bg-orange-50 text-orange-800">
          📤 Digital Outputs (Click to Toggle!)
        </h3>
        <div className="divide-y">
          {outputs && Object.entries(outputs).map(([key, value]) => (
            <div key={key} className="flex items-center justify-between px-4 py-3 hover:bg-gray-50">
              <div>
                <span className="font-medium">{key}</span>
                <span className="text-gray-500 text-sm ml-2">
                  {OUTPUT_DESCRIPTIONS[key] || ''}
                </span>
              </div>
              <BoolIndicator
                value={value}
                clickable={true}
                onClick={() => {
                  const addr = OUTPUT_ADDRESSES[key]
                  if (addr !== undefined) {
                    onToggleCoil(addr, !value, key)
                  }
                }}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Program Variables */}
      {coils && Object.keys(coils).length > 0 && (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <h3 className="text-lg font-semibold p-4 border-b bg-purple-50 text-purple-800">
            ⚙️ Program Variables
          </h3>
          <div className="divide-y">
            {Object.entries(coils).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between px-4 py-3 hover:bg-gray-50">
                <span className="font-medium">{key.replace(/_/g, ' ')}</span>
                <BoolIndicator value={value} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Registers */}
      {registers && Object.keys(registers).some(k => registers[k] !== 0) && (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <h3 className="text-lg font-semibold p-4 border-b bg-green-50 text-green-800">
            📊 Analog Values
          </h3>
          <div className="divide-y">
            {Object.entries(registers).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between px-4 py-3 hover:bg-gray-50">
                <span className="font-medium">{key.replace(/_/g, ' ')}</span>
                <span className="font-mono text-lg">{value}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default IOTable
