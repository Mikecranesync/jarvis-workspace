import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

interface ScanResult {
  ip: string
  port: number
  response_time_ms: number
}

function Setup() {
  const navigate = useNavigate()
  const [ip, setIp] = useState('192.168.1.100')
  const [connecting, setConnecting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [autoConnecting, setAutoConnecting] = useState(true)

  // Auto-connect on page load
  useEffect(() => {
    const autoConnect = async () => {
      try {
        const statusRes = await fetch('/api/plc/status')
        const status = await statusRes.json()
        
        if (status.connected) {
          navigate('/dashboard')
          return
        }

        // Try default IP
        const connectRes = await fetch('/api/plc/connect', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ ip: '192.168.1.100', port: 44818 }),
        })
        const result = await connectRes.json()
        
        if (result.success) {
          navigate('/dashboard')
        }
      } catch (e) {
        console.log('Auto-connect failed, showing manual setup')
      } finally {
        setAutoConnecting(false)
      }
    }

    autoConnect()
  }, [navigate])

  const handleConnect = async () => {
    setConnecting(true)
    setError(null)

    try {
      const response = await fetch('/api/plc/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ip, port: 44818 }),
      })

      const result = await response.json()

      if (result.success) {
        navigate('/dashboard')
      } else {
        setError(result.message || 'Connection failed')
      }
    } catch (e) {
      setError('Failed to connect to server')
    } finally {
      setConnecting(false)
    }
  }

  if (autoConnecting) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Connecting to PLC...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold text-center mb-6">
          🏭 FactoryLM Edge v4.0
        </h1>
        <p className="text-gray-600 text-center mb-6">
          Connect to your Micro820 PLC
        </p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              PLC IP Address
            </label>
            <input
              type="text"
              value={ip}
              onChange={(e) => setIp(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="192.168.1.100"
            />
          </div>

          {error && (
            <div className="bg-red-50 text-red-700 px-4 py-2 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            onClick={handleConnect}
            disabled={connecting}
            className={`w-full py-3 rounded-lg font-medium text-white transition-colors ${
              connecting
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {connecting ? 'Connecting...' : 'Connect to PLC'}
          </button>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          Using EtherNet/IP (CIP) protocol
        </div>
      </div>
    </div>
  )
}

export default Setup
