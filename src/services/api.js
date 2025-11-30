// API service for Content Generation Hub

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

class ContentHubAPI {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Health check
  async getHealth() {
    return this.request('/api/health')
  }

  // Trends
  async getTrends(limit = 10) {
    return this.request(`/api/trends?limit=${limit}`)
  }

  async addTrend(trendData) {
    return this.request('/api/trends', {
      method: 'POST',
      body: JSON.stringify(trendData),
    })
  }

  // Content
  async getContent(status = null, limit = 50) {
    const params = new URLSearchParams({ limit: limit.toString() })
    if (status) params.append('status', status)
    return this.request(`/api/content?${params}`)
  }

  async getContentItem(id) {
    return this.request(`/api/content/${id}`)
  }

  async updateContentStatus(id, status) {
    return this.request(`/api/content/${id}/status`, {
      method: 'PUT',
      body: JSON.stringify({ status }),
    })
  }

  async generateContent(data) {
    return this.request('/api/content/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async generateCustomContent(prompt, variations = 3) {
    // This will be enhanced when backend supports custom prompts
    return this.request('/api/content/generate', {
      method: 'POST',
      body: JSON.stringify({
        keyword: 'Custom Content',
        content_types: ['social_post'],
        platform: 'linkedin',
        custom_prompt: prompt,
        variations: variations
      }),
    })
  }

  // Generation
  async runGenerationCycle() {
    return this.request('/api/generate/cycle', {
      method: 'POST',
    })
  }

  // Statistics
  async getStats() {
    return this.request('/api/stats')
  }

  // Simple content generation
  async generateSimpleContent(data) {
    return this.request('/api/generate-content', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Add content to queue
  async addContentToQueue(data) {
    return this.request('/api/content', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }
}

export const api = new ContentHubAPI()

