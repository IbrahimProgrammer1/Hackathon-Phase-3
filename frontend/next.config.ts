import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone', // For production deployment
  serverExternalPackages: ['better-auth'], // Updated option name for Next.js 16+
};

export default nextConfig;