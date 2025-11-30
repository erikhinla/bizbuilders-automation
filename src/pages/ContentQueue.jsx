import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  FileText, 
  Search,
  Filter,
  CheckCircle,
  Clock,
  X,
  Eye,
  Edit
} from 'lucide-react'
import { api } from '@/services/api'

export function ContentQueue() {
  const [content, setContent] = useState([])
  const [filteredContent, setFilteredContent] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedContent, setSelectedContent] = useState(null)

  useEffect(() => {
    loadContent()
  }, [])

  useEffect(() => {
    filterContent()
  }, [content, searchTerm, statusFilter])

  const loadContent = async () => {
    try {
      setLoading(true)
      const data = await api.getContent()
      setContent(data)
    } catch (error) {
      console.error('Failed to load content:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterContent = () => {
    let filtered = [...content]

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter((item) => item.status === statusFilter)
    }

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(
        (item) =>
          item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          item.content.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    setFilteredContent(filtered)
  }

  const updateStatus = async (id, newStatus) => {
    try {
      await api.updateContentStatus(id, newStatus)
      await loadContent()
    } catch (error) {
      console.error('Failed to update status:', error)
      alert('Failed to update status')
    }
  }

  const statusOptions = [
    { value: 'all', label: 'All Status', icon: FileText },
    { value: 'draft', label: 'Draft', icon: Clock },
    { value: 'approved', label: 'Approved', icon: CheckCircle },
    { value: 'published', label: 'Published', icon: CheckCircle },
  ]

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
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content Queue</h1>
        <p className="text-gray-600 mt-1">Manage and organize your generated content</p>
      </div>

      {/* Filters */}
      <Card className="bg-white mb-6">
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <Input
                  placeholder="Search content..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              {statusOptions.map((option) => {
                const Icon = option.icon
                return (
                  <Button
                    key={option.value}
                    variant={statusFilter === option.value ? 'default' : 'outline'}
                    onClick={() => setStatusFilter(option.value)}
                    className="flex items-center space-x-2"
                  >
                    <Icon className="h-4 w-4" />
                    <span>{option.label}</span>
                  </Button>
                )
              })}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Content List */}
      {filteredContent.length === 0 ? (
        <Card className="bg-white">
          <CardContent className="py-12 text-center">
            <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p className="text-gray-500">No content found.</p>
            {searchTerm || statusFilter !== 'all' ? (
              <p className="text-sm text-gray-400 mt-2">
                Try adjusting your filters.
              </p>
            ) : (
              <p className="text-sm text-gray-400 mt-2">
                Generate some content to get started.
              </p>
            )}
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredContent.map((item) => (
            <Card key={item.id} className="bg-white">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-3">
                      <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                      <Badge
                        variant={
                          item.status === 'published'
                            ? 'default'
                            : item.status === 'approved'
                            ? 'default'
                            : 'secondary'
                        }
                      >
                        {item.status}
                      </Badge>
                      <Badge variant="outline">{item.content_type}</Badge>
                      <Badge variant="outline">{item.platform}</Badge>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-3">{item.content}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>Created: {new Date(item.created_at).toLocaleString()}</span>
                      {item.scheduled_for && (
                        <span>Scheduled: {new Date(item.scheduled_for).toLocaleString()}</span>
                      )}
                    </div>
                  </div>
                  <div className="flex flex-col space-y-2 ml-4">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setSelectedContent(item)}
                    >
                      <Eye className="h-4 w-4 mr-2" />
                      View
                    </Button>
                    {item.status === 'draft' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => updateStatus(item.id, 'approved')}
                      >
                        <CheckCircle className="h-4 w-4 mr-2" />
                        Approve
                      </Button>
                    )}
                    {item.status === 'approved' && (
                      <Button
                        variant="default"
                        size="sm"
                        onClick={() => updateStatus(item.id, 'published')}
                      >
                        Publish
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Content Detail Modal */}
      {selectedContent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <Card className="bg-white max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>{selectedContent.title}</CardTitle>
                <CardDescription>
                  {selectedContent.content_type} • {selectedContent.platform}
                </CardDescription>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedContent(null)}
              >
                <X className="h-5 w-5" />
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Content</h4>
                  <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
                    {selectedContent.content}
                  </div>
                </div>
                {selectedContent.seo_keywords && selectedContent.seo_keywords.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">SEO Keywords</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedContent.seo_keywords.map((keyword, idx) => (
                        <Badge key={idx} variant="outline">{keyword}</Badge>
                      ))}
                    </div>
                  </div>
                )}
                <div className="flex space-x-2 pt-4 border-t">
                  {selectedContent.status === 'draft' && (
                    <Button onClick={() => {
                      updateStatus(selectedContent.id, 'approved')
                      setSelectedContent(null)
                    }}>
                      Approve
                    </Button>
                  )}
                  {selectedContent.status === 'approved' && (
                    <Button onClick={() => {
                      updateStatus(selectedContent.id, 'published')
                      setSelectedContent(null)
                    }}>
                      Publish
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

