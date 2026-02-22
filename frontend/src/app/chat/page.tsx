/**
 * Chat Page
 *
 * T047: Chat page with ChatInterface and authentication check
 * Provides the main entry point for the conversational task assistant.
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChatProvider } from '@/contexts/ChatContext';
import ChatInterface from '@/components/chat/ChatInterface';

export default function ChatPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      try {
        // Check if JWT token exists in localStorage (use correct key)
        const token = localStorage.getItem('auth_token');

        if (!token) {
          setIsAuthenticated(false);
          setIsLoading(false);
          return;
        }

        // Token exists - user is authenticated
        setIsAuthenticated(true);
        setIsLoading(false);
      } catch (error) {
        console.error('Auth check error:', error);
        setIsAuthenticated(false);
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (isAuthenticated === false) {
      router.push('/auth/login?redirect=/chat');
    }
  }, [isAuthenticated, router]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="mb-4">
            <svg
              className="animate-spin h-12 w-12 text-blue-600 mx-auto"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Not authenticated - will redirect
  if (!isAuthenticated) {
    return null;
  }

  // Authenticated - show chat interface
  return (
    <ChatProvider>
      <div className="flex h-screen flex-col bg-gray-50">
        {/* Navigation bar */}
        <nav className="border-b border-gray-200 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              <div className="flex items-center gap-8">
                <h1 className="text-xl font-bold text-gray-900">Todo App</h1>
                <div className="flex gap-4">
                  <a
                    href="/tasks"
                    className="text-gray-600 hover:text-gray-900 transition-colors"
                  >
                    Tasks
                  </a>
                  <a
                    href="/chat"
                    className="text-blue-600 font-medium border-b-2 border-blue-600"
                  >
                    Chat
                  </a>
                </div>
              </div>
              <button
                onClick={() => {
                  localStorage.removeItem('auth_token');
                  router.push('/auth/login');
                }}
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </nav>

        {/* Main content */}
        <main className="flex-1 overflow-hidden">
          <div className="mx-auto h-full max-w-4xl p-4">
            <ChatInterface />
          </div>
        </main>
      </div>
    </ChatProvider>
  );
}
