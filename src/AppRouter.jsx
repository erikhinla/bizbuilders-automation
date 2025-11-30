import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ToastProvider } from './hooks/use-toast.jsx'
import { HubLayout } from './components/HubLayout'
import { Dashboard } from './pages/Dashboard'
import { ContentGenerator } from './pages/ContentGenerator'
import { ContentQueue } from './pages/ContentQueue'
import { Trends } from './pages/Trends'
import { Settings } from './pages/Settings'
import App from './App'

export function AppRouter() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          {/* Public landing page */}
          <Route path="/" element={<App />} />
          
          {/* Hub routes */}
          <Route path="/hub" element={<HubLayout />}>
            <Route index element={<Navigate to="/hub/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="generator" element={<ContentGenerator />} />
            <Route path="content" element={<ContentQueue />} />
            <Route path="trends" element={<Trends />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          
          {/* Catch all */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  )
}

