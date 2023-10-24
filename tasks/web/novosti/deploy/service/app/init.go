package app

import (
	"novosti/app/filters"
	"novosti/app/storage"
	"os"

	"github.com/revel/revel"
)

// Build variables
var (
	AppVersion string
	BuildTime  string
)

// Global state
var (
	NewsRepository *storage.NewsRepository
	AdminToken     string
)

func init() {
	revel.Filters = []revel.Filter{
		revel.PanicFilter,             // Recover from panics and display an error page instead.
		revel.RouterFilter,            // Use the routing table to select the right Action
		revel.FilterConfiguringFilter, // A hook for adding or removing per-Action filters.
		revel.ParamsFilter,            // Parse parameters into Controller.Params.
		revel.SessionFilter,           // Restore and write the session cookie.
		revel.FlashFilter,             // Restore and write the flash cookie.
		revel.ValidationFilter,        // Restore kept validation errors and save new ones from cookie.
		filters.I18nFilter,            // Resolve the requested language
		HeaderFilter,                  // Add some security based headers
		revel.InterceptorFilter,       // Run interceptors around the action.
		revel.CompressFilter,          // Compress the result.
		revel.BeforeAfterFilter,       // Call the before and after filter functions
		revel.ActionInvoker,           // Invoke the action.
	}

	revel.OnAppStart(initDB)
	revel.OnAppStart(initAdminToken)
}

func initDB() {
	directory := os.Getenv("NOVOSTI_DIR_PATH")
	if directory == "" {
		panic("NOVOSTI_DIR_PATH env var is empty, news repository will fail")
	}

	NewsRepository = storage.NewNewsRepository(directory)
}

func initAdminToken() {
	token := os.Getenv("NOVOSTI_ADMIN_TOKEN")
	if token == "" {
		panic("NOVOSTI_ADMIN_TOKEN env var is empty, admin will not be able to view shared news")
	}

	AdminToken = token
}

var HeaderFilter = func(c *revel.Controller, fc []revel.Filter) {
	c.Response.Out.Header().Add("X-Frame-Options", "SAMEORIGIN")
	c.Response.Out.Header().Add("Content-Security-Policy", "default-src 'self'; base-uri 'none'; object-src 'none'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';")

	fc[0](c, fc[1:])
}
