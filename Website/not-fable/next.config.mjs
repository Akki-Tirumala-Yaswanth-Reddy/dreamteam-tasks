/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:5000/api/:path*'
      },
    ];
  },
  // This to put images from external links, got from stack overflow.
  reactStrictMode: true,
  images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: '**',
      port: '',
      pathname: '**',
    },
    {
      protocol: 'http',
      hostname: '**',
      port: '',
      pathname: '**',
    },
  ],
},
};

export default nextConfig;
