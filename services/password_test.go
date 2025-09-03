package services

import "testing"

func TestPasswordService(t *testing.T) {
    ps := NewPasswordService()

    t.Run("Hash and Verify Success", func(t *testing.T) {
        password := "testpassword123"
        hash, err := ps.Hash(password)
        if err != nil {
            t.Fatalf("Hash failed: %v", err)
        }

        if !ps.Verify(password, hash) {
            t.Error("Verify should return true for correct password")
        }
    })

    t.Run("Verify Wrong Password", func(t *testing.T) {
        password := "testpassword123"
        hash, _ := ps.Hash(password)

        if ps.Verify("wrongpassword", hash) {
            t.Error("Verify should return false for wrong password")
        }
    })
}