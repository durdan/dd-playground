package middleware

import (
    "context"
    "encoding/json"
    "jwt-auth/services"
    "net/http"
    "strings"
)

type AuthMiddleware struct {
    jwtSvc *services.JWTService
}

func NewAuthMiddleware(jwtSvc *services.JWTService) *AuthMiddleware {
    return &AuthMiddleware{
        jwtSvc: jwtSvc,
    }
}

func (am *AuthMiddleware) RequireAuth(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        authHeader := r.Header.Get("Authorization")
        if authHeader == "" {
            am.writeError(w, "Authorization header required", http.StatusUnauthorized)
            return
        }

        tokenString := strings.TrimPrefix(authHeader, "Bearer ")
        if tokenString == authHeader {
            am.writeError(w, "Bearer token required", http.StatusUnauthorized)
            return
        }

        claims, err := am.jwtSvc.ValidateToken(tokenString)
        if err != nil {
            am.writeError(w, "Invalid token", http.StatusUnauthorized)
            return
        }

        // Add user info to request context
        ctx := context.WithValue(r.Context(), "user_id", claims.UserID)
        ctx = context.WithValue(ctx, "user_email", claims.Email)

        next.ServeHTTP(w, r.WithContext(ctx))
    }
}

func (am *AuthMiddleware) writeError(w http.ResponseWriter, message string, status int) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]string{"error": message})
}