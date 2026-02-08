'use client';

import { useState, useRef, useEffect } from 'react';
import { AuthService } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import ThemeToggle from './ThemeToggle';

export default function PremiumHeader() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  const currentUser = AuthService.getCurrentUser();

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogout = () => {
    AuthService.logout();
    router.push('/auth/login');
    router.refresh();
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="bg-gradient-to-b from-[var(--card)] to-[var(--bg)] border-b border-[var(--border)] py-4 px-4 sticky top-0 z-10 shadow-sm">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-[var(--text)]">NAFAY</h1>
              <p className="text-xs text-[var(--muted)]">Your productivity companion</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            <div className="user-dropdown" ref={dropdownRef}>
              <div
                className="avatar w-10 h-10 rounded-full bg-gradient-to-br from-[var(--primary)] to-[var(--accent)] flex items-center justify-center text-white font-semibold cursor-pointer transition-transform hover:scale-105 shadow-sm"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                {getInitials(currentUser?.name || currentUser?.email || 'User')}
              </div>

              {isDropdownOpen && (
                <div className="user-dropdown-menu">
                  <div className="p-4 border-b border-[var(--border)]">
                    <p className="font-medium text-[var(--text)]">{currentUser?.name || 'User'}</p>
                    <p className="text-sm text-[var(--muted)] truncate">{currentUser?.email}</p>
                  </div>
                  <div className="p-2">
                    <button
                      onClick={handleLogout}
                      className="w-full text-left px-3 py-2 text-sm text-[var(--error)] hover:bg-[var(--error)]/[0.1] rounded-lg transition-colors"
                    >
                      Log Out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}