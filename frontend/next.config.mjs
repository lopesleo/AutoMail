/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    if (process.env.NODE_ENV === "development") {
      return [
        {
          source: "/api/email/:path*",
          destination: `${process.env.BACKEND_URL}/email/:path*`,
        },
      ];
    }
    return [];
  },
};

export default nextConfig;
