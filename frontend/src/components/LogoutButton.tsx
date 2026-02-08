'use client';

import { useRouter } from 'next/navigation';
import { AuthService } from '@/lib/auth';

interface LogoutButtonProps {
  className?: string;
}

export default function LogoutButton({ className = '' }: LogoutButtonProps) {
  const router = useRouter();

  const handleLogout = () => {
    // Clear authentication data
    AuthService.logout();

    // Redirect to login page
    router.push('/auth/login');

    // Optionally, reload the page to ensure all state is cleared
    router.refresh();
  };

  return (
    <button
      onClick={handleLogout}
      className={`px-4 py-2 text-sm font-medium text-text hover:bg-muted rounded-lg transition-colors ${className}`}
    >
      Log Out
    </button>
  );
}