import type { NextConfig } from "next";

const apiProxyTarget = process.env.API_PROXY_TARGET ?? "http://localhost:8000";

const nextConfig: NextConfig = {
  output: "standalone",
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${apiProxyTarget}/api/v1/:path*`,
      },
    ];
  },
  // The CLI checker spawns a child `tsc` process. Use the TypeScript API so
  // builds remain reliable in sandboxed and containerized environments.
  experimental: {
    useTypeScriptCli: false,
  },
};

export default nextConfig;
