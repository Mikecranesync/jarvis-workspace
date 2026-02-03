import { useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import StatusBar from '../components/StatusBar'
import IOTable from '../components/IOTable'
import useIOStream from '../hooks/useIOStream'

interface PLCStatus {
  connected: boolean
  ip: string | null
  port: number | null
  last_seen: string | null
}

function Dashboard() {
  const navigate = useNavigate()
  const [status, setStatus] = useState<PLCStatus | null>(null)
  const [writeError, setWriteError] = useState<string | null>(null)
  const [streamEnabled, setStreamEnabled] = useState(false)

  // Use WebSocket with polling fallback
  const { ioData, isConnected, error: streamError, useWebSocket } = useIOStream(streamEnabled)

  const fetchStatus = useCallback(async () => {
    try {
      const response = await fetch('/api/plc/status')
      if (!response.ok) throw new Error('Failed to fetch status')
      const data: PLCStatus = await response.json()
      setStatus(data)
      return data.connected
    } catch (err) {
      console.error('Status fetch error:', err)
      return false
    }
  }, [])

  const handleToggleCoil = async (address: number, value: boolean, name: string) => {
    setWriteError(null)
    try {
      const response = await fetch('/api/plc/write-coil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address, value })
      })

      if (!response.ok) {
        const errData = await response.json()
        throw new Error(errData.detail || 'Write failed')
      }
    } catch (err) {
      setWriteError(err instanceof Error ? err.message : `Failed to toggle ${name}`)
    }
  }

  // Initial status check
  useEffect(() => {
    const init = async () => {
      const connected = await fetchStatus()
      if (!connected) {
        navigate('/setup')
        return
      }
      // Enable streaming after confirming connection
      setStreamEnabled(true)
    }

    init()
  }, [fetchStatus, navigate])

  // Redirect to setup if connection lost
  useEffect(() => {
    if (streamEnabled && !isConnected && streamError) {
      // Give it a moment before redirecting
      const timeout = setTimeout(() => {
        navigate('/setup')
      }, 2000)
      return () => clearTimeout(timeout)
    }
  }, [streamEnabled, isConnected, streamError, navigate])

  const displayError = writeError || streamError

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold">PLC Dashboard</h1>
          {streamEnabled && (
            <span className={`text-xs px-2 py-1 rounded ${
              useWebSocket
                ? 'bg-green-100 text-green-700'
                : 'bg-yellow-100 text-yellow-700'
            }`}>
              {useWebSocket ? 'WebSocket' : 'Polling'}
            </span>
          )}
        </div>
        <button
          onClick={() => navigate('/setup')}
          className="text-blue-600 hover:text-blue-800 font-medium"
        >
          Change Connection
        </button>
      </div>

      <StatusBar
        connected={status?.connected ?? isConnected}
        ip={status?.ip ?? null}
        port={status?.port ?? null}
        lastUpdate={ioData?.timestamp ?? null}
      />

      {displayError && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6">
          {displayError}
        </div>
      )}

      <IOTable
        coils={ioData?.coils ?? null}
        inputs={ioData?.inputs ?? null}
        outputs={ioData?.outputs ?? null}
        registers={ioData?.registers ?? null}
        onToggleCoil={handleToggleCoil}
      />
    </div>
  )
}

export default Dashboard
