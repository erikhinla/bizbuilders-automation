import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  FileText, 
  TrendingUp, 
  Settings,
  Zap,
  Building2,
  Bot,
  Menu,
  X
} from 'lucide-react'
import { Button } from './ui/button'
import { AnimatedGradientBackground } from './VideoBackground'

const brands = [
  { id: 'transformby10x', name: 'TransformBy10X', icon: Zap, colorClass: 'text-purple-600', textActiveClass: 'text-purple-700', bgClass: 'bg-purple-50', borderClass: 'border-purple-200' },
  { id: 'bizbuilders', name: 'BizBuilders', icon: Building2, colorClass: 'text-blue-600', textActiveClass: 'text-blue-700', bgClass: 'bg-blue-50', borderClass: 'border-blue-200' },
  { id: 'bizbotmarketing', name: 'BizBot Marketing', icon: Bot, colorClass: 'text-green-600', textActiveClass: 'text-green-700', bgClass: 'bg-green-50', borderClass: 'border-green-200' }
]

export function HubLayout({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [activeBrand, setActiveBrand] = useState('transformby10x')
  const location = useLocation()

  const navigation = [
    { name: 'Dashboard', href: '/hub/dashboard', icon: LayoutDashboard },
    { name: 'Content Generator', href: '/hub/generator', icon: Zap },
    { name: 'Content Queue', href: '/hub/content', icon: FileText },
    { name: 'Trends', href: '/hub/trends', icon: TrendingUp },
    { name: 'Settings', href: '/hub/settings', icon: Settings },
  ]

  const currentBrand = brands.find(b => b.id === activeBrand)

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated background */}
      <AnimatedGradientBackground className="z-0 opacity-30" />
      <div className="relative z-10 min-h-screen bg-gray-50/80 backdrop-blur-sm">
      {/* Mobile sidebar toggle */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {currentBrand && (
            <>
              <currentBrand.icon className={`h-6 w-6 ${currentBrand.colorClass}`} />
              <span className="font-bold text-gray-900">{currentBrand.name}</span>
            </>
          )}
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </Button>
      </div>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          } fixed lg:static inset-y-0 left-0 z-40 w-64 bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:translate-x-0`}
        >
          <div className="flex flex-col h-full pt-16 lg:pt-0">
            {/* Brand Selector */}
            <div className="p-4 border-b border-gray-200">
              <label className="block text-xs font-semibold text-gray-500 uppercase mb-2">
                Active Brand
              </label>
              <div className="space-y-2">
                {brands.map((brand) => {
                  const Icon = brand.icon
                  return (
                    <button
                      key={brand.id}
                      onClick={() => setActiveBrand(brand.id)}
                      className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                        activeBrand === brand.id
                          ? `${brand.bgClass} border ${brand.borderClass}`
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className={`h-5 w-5 ${brand.colorClass}`} />
                      <span className={`font-medium ${activeBrand === brand.id ? brand.textActiveClass : 'text-gray-700'}`}>
                        {brand.name}
                      </span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-1">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = location.pathname === item.href
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-purple-50 text-purple-700 border border-purple-200'
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="h-5 w-5" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                )
              })}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-gray-200">
              <div className="text-xs text-gray-500">
                <div className="font-semibold mb-1">Content Hub</div>
                <div>AI-Powered Content Generation</div>
              </div>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 lg:ml-0">
          <div className="pt-16 lg:pt-0">
            {children}
          </div>
        </main>
      </div>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

