import { useState, useEffect, useRef, useCallback } from 'react'

interface IOData {
  coils: {
    motor_running: boolean
    motor_stopped: boolean
    fault_alarm: boolean
    conveyor_running: boolean
    sensor_1_active: boolean
    sensor_2_active: boolean
    e_stop_active: boolean
  }
  inputs: {
    DI_00: boolean
    DI_01: boolean
    DI_02: boolean
    DI_03: boolean
    DI_04: boolean
    DI_05: boolean
    DI_06: boolean
    DI_07: boolean
  }
  outputs: {
    DO_00: boolean
    DO_01: boolean
    DO_03: boolean
  }
  registers: {
    motor_speed: number
    motor_current: number
    temperature: number
    pressure: number
    conveyor_speed: number
    error_code: number
  }
  timestamp: string
  error?: string
  connected?: boolean
}

interface UseIOStreamResult {
  ioData: IOData | null
  isConnected: boolean
  error: string | null
  useWebSocket: boolean
}

export function useIOStream(enabled: boolean = true): UseIOStreamResult {
  const [ioData, setIoData] = useState<IOData | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [useWebSocket, setUseWebSocket] = useState(false)

  const wsRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<number | null>(null)
  const pollingIntervalRef = useRef<number | null>(null)

  // Fallback to polling
  const startPolling = useCallback(() => {
    if (pollingIntervalRef.current) return

    const poll = async () => {
      try {
        const response = await fetch('/api/plc/io')
        if (!response.ok) {
          if (response.status === 503) {
            setIsConnected(false)
            setError('Not connected to PLC')
            return
          }
          throw new Error('Failed to fetch I/O')
        }
        const data: IOData = await response.json()
        setIoData(data)
        setIsConnected(true)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      }
    }

    poll() // Initial poll
    pollingIntervalRef.current = window.setInterval(poll, 500)
  }, [])

  const stopPolling = useCallback(() => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current)
      pollingIntervalRef.current = null
    }
  }, [])

  // WebSocket connection
  const connectWebSocket = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return

    // Construct WebSocket URL
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const wsUrl = `${protocol}//${host}/ws/io`

    try {
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log('WebSocket connected')
        setUseWebSocket(true)
        setIsConnected(true)
        setError(null)
        stopPolling() // Stop polling when WebSocket connects
      }

      ws.onmessage = (event) => {
        try {
          const data: IOData = JSON.parse(event.data)
          if (data.error) {
            setError(data.error)
            setIsConnected(data.connected ?? false)
          } else {
            setIoData(data)
            setIsConnected(true)
            setError(null)
          }
        } catch {
          console.error('Failed to parse WebSocket message')
        }
      }

      ws.onerror = () => {
        console.log('WebSocket error, falling back to polling')
        setUseWebSocket(false)
        startPolling()
      }

      ws.onclose = () => {
        console.log('WebSocket closed')
        setUseWebSocket(false)
        wsRef.current = null

        // Attempt reconnect after 3 seconds
        if (enabled) {
          startPolling() // Start polling immediately
          reconnectTimeoutRef.current = window.setTimeout(() => {
            connectWebSocket()
          }, 3000)
        }
      }

      wsRef.current = ws
    } catch {
      console.log('WebSocket not available, using polling')
      setUseWebSocket(false)
      startPolling()
    }
  }, [enabled, startPolling, stopPolling])

  useEffect(() => {
    if (!enabled) {
      // Cleanup
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
      stopPolling()
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      return
    }

    // Try WebSocket first
    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
      stopPolling()
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
    }
  }, [enabled, connectWebSocket, stopPolling])

  return { ioData, isConnected, error, useWebSocket }
}

export default useIOStream
