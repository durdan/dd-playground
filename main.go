package main

import (
    "encoding/json"
    "jwt-auth/middleware"
    "jwt-auth/models"
    "jwt-auth/services"
    "log"
    "net/http"
)

type Server struct {
    authSvc    *services.AuthService
    authMiddleware *middleware.AuthMiddleware
}

func main() {
    // Initialize services
    passwordSvc := services.NewPasswordService()
    jwtSvc := services.NewJWTService("your-secret-key-change-in-production")
    authSvc := services.NewAuthService(passwordSvc, jwtSvc)
    authMiddleware := middleware.NewAuthMiddleware(jwtSvc, authSvc)

    server := &Server{
        authSvc:        authSvc,
        authMiddleware: authMiddleware,
    }

    // Routes
    http.HandleFunc("/register", server.handleRegister)
    http.HandleFunc("/login", server.handleLogin)
    http.HandleFunc("/profile", server.authMiddleware.RequireAuth(server.handleProfile))

    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func (s *Server) handleRegister(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        s.writeError(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req models.RegisterRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        s.writeError(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    user, token, err := s.authSvc.Register(&req)
    if err != nil {
        s.writeError(w, err.Error(), http.StatusBadRequest)
        return
    }

    response := map[string]interface{}{
        "user":  user,
        "token": token,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (s *Server) handleLogin(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        s.writeError(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req models.LoginRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        s.writeError(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    user, token, err := s.authSvc.Login(&req)
    if err != nil {
        s.writeError(w, err.Error(), http.StatusUnauthorized)
        return
    }

    response := map[string]interface{}{
        "user":  user,
        "token": token,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (s *Server) handleProfile(w http.ResponseWriter, r *http.Request) {
    user := r.Context().Value(middleware.UserContextKey).(*models.User)
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "message": "Protected route accessed successfully",
        "user":    user,
    })
}

func (s *Server) writeError(w http.ResponseWriter, message string, status int) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]string{"error": message})
}