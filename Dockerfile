# Build Stage
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Copy the server directory content
COPY server/ ./server/

# Build the Go application from the server directory
WORKDIR /app/server
RUN go mod tidy
RUN go build -o yawstar-server .

# Run Stage
FROM alpine:latest
WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/server/yawstar-server .

EXPOSE 8080
CMD ["./yawstar-server", "-host=0.0.0.0", "-port=8080"]