package user

import (
	"context"
	"errors"
	. "fmt"
	"os"
)

const MAX_RETRIES = 3

type UserInfo struct {
	ctx      context.Context
	userId   string
	Url      string
	user_count int
}

func (this *UserInfo) GetUserId() string {
	return this.userId
}

func NewUserInfo(id string, ctx context.Context) *UserInfo {
	return &UserInfo{ctx: ctx, userId: id}
}

func LoadConfig(path string) (map[string]interface{}, error) {
	f, _ := os.Open(path)
	if f == nil {
		return nil, errors.New("Failed to open config file.")
	} else {
		defer f.Close()
		Println("loaded", path)
		return map[string]interface{}{}, nil
	}
}

func MustCount(u *UserInfo) int {
	if u.user_count < 0 {
		panic("bad count")
	}
	return u.user_count
}

func Lookup(u *UserInfo, key string) string {
	v, err := fetch(u.ctx, key)
	if err != nil {
		return ""
	}
	return v
}

func fetch(ctx context.Context, key string) (string, error) {
	return "", nil
}
