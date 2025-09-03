package services

import (
    "errors"
    "jwt-auth/models"
    "sync"
)

type AuthService struct {
    users       map[string]*models.User // email -> user
    usersByID   map[int]*models.User    // id -> user
    nextID      int
    mu          sync.RWMutex
    passwordSvc *PasswordService
    jwtSvc      *JWTService
}

func NewAuthService(passwordSvc *PasswordService, jwtSvc *JWTService) *AuthService {
    return &AuthService{
        users:       make(map[string]*models.User),
        usersByID:   make(map[int]*models.User),
        nextID:      1,
        passwordSvc: passwordSvc,
        jwtSvc:      jwtSvc,
    }
}

func (as *AuthService) Register(req *models.RegisterRequest) (string, error) {
    if err := req.Validate(); err != nil {
        return "", err
    }

    as.mu.Lock()
    defer as.mu.Unlock()

    if _, exists := as.users[req.Email]; exists {
        return "", errors.New("user already exists")
    }

    hashedPassword, err := as.passwordSvc.Hash(req.Password)
    if err != nil {
        return "", err
    }

    user := &models.User{
        ID:       as.nextID,
        Email:    req.Email,
        Password: hashedPassword,
    }

    as.users[req.Email] = user
    as.usersByID[as.nextID] = user
    as.nextID++

    return as.jwtSvc.GenerateToken(user.ID, user.Email)
}

func (as *AuthService) Login(req *models.LoginRequest) (string, error) {
    if err := req.Validate(); err != nil {
        return "", err
    }

    as.mu.RLock()
    user, exists := as.users[req.Email]
    as.mu.RUnlock()

    if !exists {
        return "", errors.New("invalid credentials")
    }

    if !as.passwordSvc.Verify(req.Password, user.Password) {
        return "", errors.New("invalid credentials")
    }

    return as.jwtSvc.GenerateToken(user.ID, user.Email)
}

func (as *AuthService) GetUserByID(id int) (*models.User, error) {
    as.mu.RLock()
    defer as.mu.RUnlock()

    user, exists := as.usersByID[id]
    if !exists {
        return nil, errors.New("user not found")
    }

    return user, nil
}