import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  Sparkles,
  Copy,
  CheckCircle,
  Loader2,
  Save,
  Plus
} from 'lucide-react'
import { api } from '@/services/api'
import { useToast } from '@/hooks/use-toast'

export function ContentGenerator() {
  const [formData, setFormData] = useState({
    topic: '',
    channel: 'linkedin',
    count: 3,
  })
  
  const [generatedPosts, setGeneratedPosts] = useState([])
  const [loading, setLoading] = useState(false)
  const [copiedIndex, setCopiedIndex] = useState(null)
  const [savingIndex, setSavingIndex] = useState(null)
  const { toast } = useToast()

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleGenerate = async (e) => {
    e?.preventDefault()
    
    if (!formData.topic.trim()) {
      toast({
        title: 'Topic required',
        description: 'Please enter a topic before generating content.',
        variant: 'destructive'
      })
      return
    }

    setLoading(true)
    setGeneratedPosts([])
    
    try {
      const result = await api.generateSimpleContent({
        topic: formData.topic,
        channel: formData.channel,
        count: parseInt(formData.count) || 3
      })
      
      if (result.posts && result.posts.length > 0) {
        setGeneratedPosts(result.posts)
        toast({
          title: 'Content generated!',
          description: `Successfully generated ${result.posts.length} posts.`,
        })
      } else {
        toast({
          title: 'No content generated',
          description: 'The API returned no posts. Please try again.',
          variant: 'destructive'
        })
      }
    } catch (error) {
      console.error('Generation failed:', error)
      toast({
        title: 'Generation failed',
        description: error.message || 'Failed to generate content. Please try again.',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSaveToQueue = async (post, index) => {
    setSavingIndex(index)
    try {
      await api.addContentToQueue({
        title: `Generated: ${formData.topic}`,
        content: post.text,
        content_type: 'social_post',
        platform: formData.channel,
        status: 'draft',
        seo_keywords: [formData.topic],
        metadata: {
          generated_from: 'content_generator',
          topic: formData.topic
        }
      })
      
      toast({
        title: 'Saved to queue!',
        description: 'Content has been added to your content queue.',
      })
    } catch (error) {
      console.error('Save failed:', error)
      toast({
        title: 'Save failed',
        description: error.message || 'Failed to save to queue. Please try again.',
        variant: 'destructive'
      })
    } finally {
      setSavingIndex(null)
    }
  }


  const copyToClipboard = async (text, index) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className="p-6 lg:p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Content Generator</h1>
        <p className="text-gray-600 mt-1">Generate custom social media posts with AI</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <Card className="bg-white">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5" />
              <span>Generate Content</span>
            </CardTitle>
            <CardDescription>Enter a topic and generate posts</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleGenerate} className="space-y-6">
              {/* Topic */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Topic
                </label>
                <Input
                  type="text"
                  value={formData.topic}
                  onChange={(e) => handleChange('topic', e.target.value)}
                  placeholder="e.g., AI automation, business growth, productivity"
                  required
                />
              </div>

              {/* Channel */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Channel
                </label>
                <select
                  value={formData.channel}
                  onChange={(e) => handleChange('channel', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="linkedin">LinkedIn</option>
                  <option value="twitter">Twitter</option>
                  <option value="facebook">Facebook</option>
                  <option value="instagram">Instagram</option>
                  <option value="blog">Blog</option>
                </select>
              </div>

              {/* Count */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Posts
                </label>
                <Input
                  type="number"
                  min="1"
                  max="10"
                  value={formData.count}
                  onChange={(e) => handleChange('count', e.target.value)}
                  placeholder="3"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">Generate 1-10 posts</p>
              </div>

              {/* Generate Button */}
              <Button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4 mr-2" />
                    Generate
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Generated Posts */}
        <div className="space-y-4">
          {generatedPosts.length === 0 ? (
            <Card className="bg-white">
              <CardContent className="py-12 text-center">
                <Sparkles className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p className="text-gray-500">Generated posts will appear here</p>
                <p className="text-sm text-gray-400 mt-2">
                  Configure your parameters and click "Generate 3 Variations"
                </p>
              </CardContent>
            </Card>
          ) : (
            generatedPosts.map((post, index) => (
              <Card key={post.id || index} className="bg-white">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <CardTitle className="text-lg">Post {index + 1}</CardTitle>
                    <Badge variant="outline">{post.channel || formData.channel}</Badge>
                  </div>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => copyToClipboard(post.text || post.content || post, index)}
                    >
                      {copiedIndex === index ? (
                        <>
                          <CheckCircle className="h-4 w-4 mr-2 text-green-600" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="h-4 w-4 mr-2" />
                          Copy
                        </>
                      )}
                    </Button>
                    <Button
                      variant="default"
                      size="sm"
                      onClick={() => handleSaveToQueue(post, index)}
                      disabled={savingIndex === index}
                      className="bg-green-600 hover:bg-green-700"
                    >
                      {savingIndex === index ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Saving...
                        </>
                      ) : (
                        <>
                          <Save className="h-4 w-4 mr-2" />
                          Save to Queue
                        </>
                      )}
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="bg-gray-50 p-4 rounded-lg whitespace-pre-wrap text-sm">
                    {post.text || post.content || post}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  )
}





