import { NextRequest, NextResponse } from 'next/server';

// Middleware to protect routes that require authentication
export function middleware(request: NextRequest) {
  // Define protected routes
  const protectedRoutes = ['/tasks', '/profile'];
  const isProtectedRoute = protectedRoutes.some(route =>
    request.nextUrl.pathname.startsWith(route)
  );

  // Check if user is authenticated (simplified - in real app, verify JWT)
  const token = request.cookies.get('auth_token')?.value ||
                request.headers.get('authorization')?.replace('Bearer ', '');

  if (isProtectedRoute && !token) {
    // Redirect to login if not authenticated
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  return NextResponse.next();
}

// Define which routes the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};