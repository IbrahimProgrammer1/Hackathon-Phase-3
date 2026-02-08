'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { AuthService } from '@/lib/auth';

export default function HomePage() {
  const [isAuthed, setIsAuthed] = useState(false);

  useEffect(() => {
    setIsAuthed(AuthService.isAuthenticated());
  }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-3xl px-6 py-16">
        <div className="rounded-2xl bg-white p-8 shadow-sm ring-1 ring-gray-200">
          <h1 className="text-3xl font-bold text-gray-900">Todo App</h1>
          <p className="mt-2 text-gray-600">
            Secure, multi-user todo application (Phase II)
          </p>

          <div className="mt-8 grid gap-3 sm:grid-cols-2">
            {isAuthed ? (
              <Link
                href="/tasks"
                className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
              >
                Open dashboard
              </Link>
            ) : (
              <>
                <Link
                  href="/auth/login"
                  className="inline-flex items-center justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700"
                >
                  Sign in
                </Link>
                <Link
                  href="/auth/register"
                  className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-50"
                >
                  Create account
                </Link>
              </>
            )}
          </div>

          <div className="mt-10 border-t border-gray-200 pt-6 text-sm text-gray-500">
            <p>
              Tip: after signing in, you’ll be redirected to{' '}
              <code className="rounded bg-gray-100 px-1.5 py-0.5 text-gray-700">
                /tasks
              </code>
              .
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
