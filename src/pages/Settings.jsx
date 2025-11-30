import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Settings as SettingsIcon, Save, Key } from 'lucide-react'

export function Settings() {
  const [settings, setSettings] = useState({
    apiUrl: 'http://localhost:5000',
    openaiApiKey: '',
    generationInterval: 2,
    maxContentPerCycle: 5,
  })
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    // Load settings from localStorage
    const savedSettings = localStorage.getItem('contentHubSettings')
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings))
    }
  }, [])

  const handleSave = () => {
    localStorage.setItem('contentHubSettings', JSON.stringify(settings))
    setSaved(true)
    setTimeout(() => setSaved(false), 2000)
  }

  return (
    <div className="p-6 lg:p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Configure your content generation hub</p>
      </div>

      <div className="space-y-6">
        {/* API Configuration */}
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Key className="h-5 w-5" />
              <span>API Configuration</span>
            </CardTitle>
            <CardDescription>
              Configure API endpoints and keys
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                API Base URL
              </label>
              <Input
                value={settings.apiUrl}
                onChange={(e) => setSettings({ ...settings, apiUrl: e.target.value })}
                placeholder="http://localhost:5000"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                OpenAI API Key
              </label>
              <Input
                type="password"
                value={settings.openaiApiKey}
                onChange={(e) => setSettings({ ...settings, openaiApiKey: e.target.value })}
                placeholder="sk-..."
              />
              <p className="text-xs text-gray-500 mt-1">
                Leave empty to use environment variable
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Generation Settings */}
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <SettingsIcon className="h-5 w-5" />
              <span>Generation Settings</span>
            </CardTitle>
            <CardDescription>
              Configure content generation behavior
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Generation Interval (hours)
              </label>
              <Input
                type="number"
                value={settings.generationInterval}
                onChange={(e) => setSettings({ ...settings, generationInterval: parseInt(e.target.value) })}
                min="1"
              />
              <p className="text-xs text-gray-500 mt-1">
                How often to automatically generate content
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Content Per Cycle
              </label>
              <Input
                type="number"
                value={settings.maxContentPerCycle}
                onChange={(e) => setSettings({ ...settings, maxContentPerCycle: parseInt(e.target.value) })}
                min="1"
                max="20"
              />
              <p className="text-xs text-gray-500 mt-1">
                Maximum number of content pieces to generate per cycle
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Save Button */}
        <div className="flex justify-end">
          <Button onClick={handleSave} className="min-w-[120px]">
            <Save className="h-4 w-4 mr-2" />
            {saved ? 'Saved!' : 'Save Settings'}
          </Button>
        </div>
      </div>
    </div>
  )
}

