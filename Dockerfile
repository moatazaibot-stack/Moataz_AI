# Moataz AI v1.0 — Production Dockerfile
# Multi-stage build for minimal production image

FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat openssl
WORKDIR /app

# Install dependencies
FROM base AS deps
COPY package.json bun.lock ./
COPY prisma ./prisma/
RUN npm install -g bun && bun install --frozen-lockfile

# Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npx prisma generate
RUN npm run build

# Production image — minimal footprint
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

LABEL org.opencontainers.image.title="Moataz AI"
LABEL org.opencontainers.image.description="Enterprise AI Operating System"
LABEL org.opencontainers.image.version="1.0.0"

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 moataz

COPY --from=builder /app/public ./public
COPY --from=builder --chown=moataz:nodejs /app/.next/standalone ./
COPY --from=builder --chown=moataz:nodejs /app/.next/static ./.next/static
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/node_modules/.prisma ./node_modules/.prisma
COPY --from=builder /app/node_modules/@prisma ./node_modules/@prisma
COPY --from=builder /app/node_modules/prisma ./node_modules/prisma
COPY --from=builder /app/scripts/start.sh ./scripts/start.sh

USER moataz
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/v1/health || exit 1

CMD ["sh", "./scripts/start.sh"]
