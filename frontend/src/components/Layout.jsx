import { Link, Outlet, useLocation } from 'react-router-dom'
import { LayoutDashboard, FileText, BookOpen, Settings as SettingsIcon, LogOut } from 'lucide-react'

const NavItem = ({ to, icon: Icon, children }) => {
  const location = useLocation()
  const isActive = location.pathname === to
  
  return (
    <Link 
      to={to} 
      className={`flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${isActive ? 'bg-gray-100 border-r-4 border-blue-500' : ''}`}
    >
      <Icon className="w-5 h-5 mr-3" />
      <span>{children}</span>
    </Link>
  )
}

export default function Layout() {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r shadow-sm flex flex-col">
        <div className="p-6 border-b">
          <h1 className="text-2xl font-bold text-blue-600">zer0-pages</h1>
        </div>
        <nav className="flex-1 mt-6">
          <NavItem to="/" icon={LayoutDashboard}>Dashboard</NavItem>
          <NavItem to="/posts" icon={FileText}>Posts</NavItem>
          <NavItem to="/pages" icon={FileText}>Pages</NavItem>
          <NavItem to="/prds" icon={BookOpen}>PRDs</NavItem>
          <NavItem to="/settings" icon={SettingsIcon}>Settings</NavItem>
        </nav>
        <div className="p-4 border-t">
          <button className="flex items-center w-full px-4 py-2 text-gray-600 hover:text-red-600">
            <LogOut className="w-5 h-5 mr-3" />
            Logout
          </button>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white border-b h-16 flex items-center justify-between px-8">
          <h2 className="text-xl font-semibold text-gray-800">Dashboard</h2>
          <div className="flex items-center space-x-4">
            {/* User profile, etc */}
            <div className="w-8 h-8 rounded-full bg-gray-200"></div>
          </div>
        </header>
        <main className="p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

