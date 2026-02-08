'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode; // Component to show while checking auth status
  unauthorizedRedirect?: string; // Where to redirect if not authorized (default: '/auth/login')
}

export default function ProtectedRoute({
  children,
  fallback = <div className="p-4">Checking authentication...</div>,
  unauthorizedRedirect = '/auth/login'
}: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null); // null = checking
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      // In a real implementation, you would check for the auth token
      // For now, we'll simulate the authentication process
      const token = localStorage.getItem('auth_token');
      const authStatus = token !== null && token !== '';
      setIsAuthenticated(authStatus);

      if (!authStatus) {
        // Redirect to login if not authenticated
        router.push(unauthorizedRedirect);
      }
    };

    checkAuth();
  }, [router, unauthorizedRedirect]);

  // While checking auth status
  if (isAuthenticated === null) {
    return fallback;
  }

  // If authenticated, render children
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // If not authenticated, return fallback (which will likely be replaced by redirect)
  return fallback;
}