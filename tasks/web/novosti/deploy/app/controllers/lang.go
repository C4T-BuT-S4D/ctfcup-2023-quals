package controllers

import (
	"net/http"
	"novosti/app/routes"

	"github.com/revel/revel"
)

// Lang enables i18n by changing the user's language.
type Lang struct {
	*revel.Controller
}

// Locale saves the new chosen locale.
func (c Lang) Locale() revel.Result {
	locale := c.Params.Query.Get("locale")

	c.SetCookie(&http.Cookie{
		Name:     revel.CookiePrefix + "_LANG",
		Value:    locale,
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
	})

	return c.Redirect(routes.News.Share())
}
