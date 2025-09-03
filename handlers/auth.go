package handlers

import (
    "encoding/json"
    "jwt-auth/models"
    "jwt-auth/services"
    "net/http"
)

type AuthHandler struct {
    authSvc *services.AuthService
}

func NewAuthHandler(authSvc *services.AuthService) *AuthHandler {
    return &AuthHandler{authSvc: authSvc}
}

func (ah *AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        ah.writeError(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req models.RegisterRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        ah.writeError(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    user, token, err := ah.authSvc.Register(&req)
    if err != nil {
        ah.writeError(w, err.Error(), http.StatusBadRequest)
        return
    }

    response := map[string]interface{}{
        "user":  user,
        "token": token,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (ah *AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        ah.writeError(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req models.LoginRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        ah.writeError(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    user, token, err := ah.authSvc.Login(&req)
    if err != nil {
        ah.writeError(w, err.Error(), http.StatusUnauthorized)
        return
    }

    response := map[string]interface{}{
        "user":  user,
        "token": token,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (ah *AuthHandler) Profile(w http.ResponseWriter, r *http.Request) {
    user := r.Context().Value("user").(*models.User)
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "user": user,
    })
}

func (ah *AuthHandler) writeError(w http.ResponseWriter, message string, status int) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(map[string]string{"error": message})
}