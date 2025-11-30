import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  TrendingUp, 
  Plus,
  Zap,
  BarChart3
} from 'lucide-react'
import { api } from '@/services/api'

export function Trends() {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newTrend, setNewTrend] = useState({
    keyword: '',
    volume: 1000,
    growth_rate: 0.1,
    platform: 'transformby10x',
    relevance_score: 0.8,
  })
  const [generating, setGenerating] = useState({})

  useEffect(() => {
    loadTrends()
  }, [])

  const loadTrends = async () => {
    try {
      setLoading(true)
      const data = await api.getTrends(50)
      setTrends(data)
    } catch (error) {
      console.error('Failed to load trends:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddTrend = async (e) => {
    e.preventDefault()
    try {
      await api.addTrend({
        ...newTrend,
        source: 'manual',
      })
      setShowAddForm(false)
      setNewTrend({
        keyword: '',
        volume: 1000,
        growth_rate: 0.1,
        platform: 'transformby10x',
        relevance_score: 0.8,
      })
      await loadTrends()
    } catch (error) {
      console.error('Failed to add trend:', error)
      alert('Failed to add trend')
    }
  }

  const handleGenerateContent = async (trend) => {
    try {
      setGenerating({ ...generating, [trend.keyword]: true })
      await api.generateContent({
        keyword: trend.keyword,
        content_types: ['social_post', 'blog_post'],
        platform: trend.platform,
        volume: trend.volume,
        growth_rate: trend.growth_rate,
        relevance_score: trend.relevance_score,
      })
      alert('Content generated successfully!')
    } catch (error) {
      console.error('Failed to generate content:', error)
      alert('Failed to generate content')
    } finally {
      setGenerating({ ...generating, [trend.keyword]: false })
    }
  }

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Trends</h1>
          <p className="text-gray-600 mt-1">Monitor and generate content from trending topics</p>
        </div>
        <Button onClick={() => setShowAddForm(!showAddForm)}>
          <Plus className="h-4 w-4 mr-2" />
          Add Trend
        </Button>
      </div>

      {/* Add Trend Form */}
      {showAddForm && (
        <Card className="bg-white mb-6">
          <CardHeader>
            <CardTitle>Add New Trend</CardTitle>
            <CardDescription>Add a trend to generate content from</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddTrend} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Keyword/Topic
                </label>
                <Input
                  value={newTrend.keyword}
                  onChange={(e) => setNewTrend({ ...newTrend, keyword: e.target.value })}
                  placeholder="e.g., AI-powered business automation"
                  required
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Volume
                  </label>
                  <Input
                    type="number"
                    value={newTrend.volume}
                    onChange={(e) => setNewTrend({ ...newTrend, volume: parseInt(e.target.value) })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Growth Rate
                  </label>
                  <Input
                    type="number"
                    step="0.01"
                    value={newTrend.growth_rate}
                    onChange={(e) => setNewTrend({ ...newTrend, growth_rate: parseFloat(e.target.value) })}
                    required
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Platform
                  </label>
                  <select
                    value={newTrend.platform}
                    onChange={(e) => setNewTrend({ ...newTrend, platform: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    <option value="transformby10x">TransformBy10X</option>
                    <option value="bizbuilders">BizBuilders</option>
                    <option value="bizbotmarketing">BizBot Marketing</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Relevance Score
                  </label>
                  <Input
                    type="number"
                    step="0.01"
                    min="0"
                    max="1"
                    value={newTrend.relevance_score}
                    onChange={(e) => setNewTrend({ ...newTrend, relevance_score: parseFloat(e.target.value) })}
                    required
                  />
                </div>
              </div>
              <div className="flex space-x-3">
                <Button type="submit">Add Trend</Button>
                <Button type="button" variant="outline" onClick={() => setShowAddForm(false)}>
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Trends List */}
      {trends.length === 0 ? (
        <Card className="bg-white">
          <CardContent className="py-12 text-center">
            <TrendingUp className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p className="text-gray-500">No trends found.</p>
            <p className="text-sm text-gray-400 mt-2">
              Add a trend to start generating content.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {trends.map((trend) => (
            <Card key={trend.keyword} className="bg-white">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{trend.keyword}</CardTitle>
                    <CardDescription className="mt-1">
                      {trend.platform} • {trend.source}
                    </CardDescription>
                  </div>
                  <Badge
                    variant={trend.relevance_score > 0.8 ? 'default' : 'secondary'}
                  >
                    {Math.round(trend.relevance_score * 100)}%
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Volume:</span>
                    <span className="font-semibold">{trend.volume.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Growth:</span>
                    <span className="font-semibold text-green-600">
                      +{(trend.growth_rate * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="pt-3 border-t">
                    <Button
                      className="w-full"
                      onClick={() => handleGenerateContent(trend)}
                      disabled={generating[trend.keyword]}
                    >
                      <Zap className={`h-4 w-4 mr-2 ${generating[trend.keyword] ? 'animate-spin' : ''}`} />
                      {generating[trend.keyword] ? 'Generating...' : 'Generate Content'}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

