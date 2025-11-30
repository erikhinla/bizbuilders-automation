import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  FileText, 
  TrendingUp, 
  CheckCircle, 
  Clock, 
  Zap,
  BarChart3,
  Plus,
  RefreshCw
} from 'lucide-react'
import { api } from '@/services/api'

export function Dashboard() {
  const [stats, setStats] = useState(null)
  const [recentContent, setRecentContent] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [statsData, contentData] = await Promise.all([
        api.getStats(),
        api.getContent(null, 5)
      ])
      setStats(statsData)
      setRecentContent(contentData)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    try {
      setGenerating(true)
      await api.runGenerationCycle()
      await loadData() // Refresh data
    } catch (error) {
      console.error('Generation failed:', error)
      alert('Failed to run generation cycle. Check console for details.')
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <div className="p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  const statCards = [
    {
      title: 'Total Content',
      value: stats?.total_content || 0,
      icon: FileText,
      colorClass: 'text-blue-600',
    },
    {
      title: 'Draft',
      value: stats?.by_status?.draft || 0,
      icon: Clock,
      colorClass: 'text-yellow-600',
    },
    {
      title: 'Published',
      value: stats?.by_status?.published || 0,
      icon: CheckCircle,
      colorClass: 'text-green-600',
    },
    {
      title: 'Trends',
      value: stats?.by_platform ? Object.keys(stats.by_platform).length : 0,
      icon: TrendingUp,
      colorClass: 'text-purple-600',
    },
  ]

  return (
    <div className="p-6 lg:p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Content Hub Dashboard</h1>
          <p className="text-gray-600 mt-1">AI-powered content generation and management</p>
        </div>
        <div className="flex space-x-3">
          <Button
            variant="outline"
            onClick={loadData}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button
            onClick={handleGenerate}
            disabled={generating}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
          >
            <Zap className={`h-4 w-4 mr-2 ${generating ? 'animate-spin' : ''}`} />
            {generating ? 'Generating...' : 'Generate Content'}
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((stat) => {
          const Icon = stat.icon
          return (
            <Card key={stat.title} className="bg-white">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">
                  {stat.title}
                </CardTitle>
                <Icon className={`h-5 w-5 ${stat.colorClass}`} />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Recent Content */}
      <Card className="bg-white">
        <CardHeader>
          <CardTitle>Recent Content</CardTitle>
          <CardDescription>Latest generated content pieces</CardDescription>
        </CardHeader>
        <CardContent>
          {recentContent.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No content generated yet.</p>
              <p className="text-sm mt-2">Click "Generate Content" to get started.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {recentContent.map((content) => (
                <div
                  key={content.id}
                  className="flex items-start justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="font-semibold text-gray-900">{content.title}</h3>
                      <Badge
                        variant={
                          content.status === 'published'
                            ? 'default'
                            : content.status === 'draft'
                            ? 'secondary'
                            : 'outline'
                        }
                      >
                        {content.status}
                      </Badge>
                      <Badge variant="outline">{content.content_type}</Badge>
                      <Badge variant="outline">{content.platform}</Badge>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {content.content}
                    </p>
                    <p className="text-xs text-gray-400 mt-2">
                      Created: {new Date(content.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Platform Distribution */}
      {stats?.by_platform && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
          <Card className="bg-white">
            <CardHeader>
              <CardTitle>By Platform</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(stats.by_platform).map(([platform, count]) => (
                  <div key={platform} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700 capitalize">
                      {platform}
                    </span>
                    <Badge>{count}</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white">
            <CardHeader>
              <CardTitle>By Content Type</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {stats.by_type &&
                  Object.entries(stats.by_type).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700 capitalize">
                        {type.replace('_', ' ')}
                      </span>
                      <Badge>{count}</Badge>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

