package main

import (
    "jwt-auth/handlers"
    "jwt-auth/middleware"
    "jwt-auth/services"
    "log"
    "net/http"
)

func main() {
    // Initialize services
    passwordSvc := services.NewPasswordService()
    jwtSvc := services.NewJWTService("your-secret-key-change-in-production")
    authSvc := services.NewAuthService(passwordSvc, jwtSvc)

    // Initialize handlers and middleware
    authHandler := handlers.NewAuthHandler(authSvc)
    authMiddleware := middleware.NewAuthMiddleware(jwtSvc, authSvc)

    // Routes
    http.HandleFunc("/register", authHandler.Register)
    http.HandleFunc("/login", authHandler.Login)
    http.HandleFunc("/profile", authMiddleware.RequireAuth(authHandler.Profile))

    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}