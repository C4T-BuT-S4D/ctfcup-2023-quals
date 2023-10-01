package controllers

import (
	"github.com/revel/revel"
)

type App struct {
	*revel.Controller
}

func (c App) Share() revel.Result {
	return c.Render()
}
