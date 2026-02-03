interface StatusBarProps {
  connected: boolean
  ip: string | null
  port: number | null
  lastUpdate: string | null
}

function StatusBar({ connected, ip, port, lastUpdate }: StatusBarProps) {
  return (
    <div className="bg-white shadow rounded-lg p-4 mb-6 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span
            className={`w-3 h-3 rounded-full ${
              connected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span className="font-medium">
            {connected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        {ip && (
          <span className="text-gray-500">
            {ip}:{port}
          </span>
        )}
      </div>
      {lastUpdate && (
        <span className="text-sm text-gray-400">
          Last update: {new Date(lastUpdate).toLocaleTimeString()}
        </span>
      )}
    </div>
  )
}

export default StatusBar
