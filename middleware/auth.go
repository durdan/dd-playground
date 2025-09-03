package middleware

import (
    "context"
    "encoding/json"
    "jwt-auth/services"
    "net/http"
    "strings"
)

type AuthMiddleware struct {
    jwtSvc  *JWTService
    authSvc *AuthService
}

func NewAuthMiddleware(jwtSvc *services.JWTService, authSvc *services.AuthService) *AuthMiddleware {
    return &AuthMiddleware{
        jwtSvc:  jwtSvc,
        authSvc: authSvc,
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

        user, err := am.authSvc.GetUserByID(claims.UserID)
        if err != nil {
            am.writeError(w, "User not found", http.StatusUnauthorized)
            return
        }

        ctx := context.WithValue(r.Context(), "user", user)
        next.ServeHTTP(w, r.WithContext(ctx))
    }
}

func (am *AuthMiddleware) writeError(w http.ResponseWriter, message string, status int) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]string{"error": message})
}