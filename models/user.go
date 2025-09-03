package models

import (
    "errors"
    "regexp"
)

type User struct {
    ID       int    `json:"id"`
    Email    string `json:"email"`
    Password string `json:"-"` // Never serialize password
}

type LoginRequest struct {
    Email    string `json:"email"`
    Password string `json:"password"`
}

type RegisterRequest struct {
    Email    string `json:"email"`
    Password string `json:"password"`
}

func (r *RegisterRequest) Validate() error {
    if r.Email == "" {
        return errors.New("email is required")
    }
    if r.Password == "" {
        return errors.New("password is required")
    }
    if len(r.Password) < 6 {
        return errors.New("password must be at least 6 characters")
    }
    
    emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
    if !emailRegex.MatchString(r.Email) {
        return errors.New("invalid email format")
    }
    
    return nil
}

func (r *LoginRequest) Validate() error {
    if r.Email == "" {
        return errors.New("email is required")
    }
    if r.Password == "" {
        return errors.New("password is required")
    }
    return nil
}