package controllers

import (
	"net/http"
	"novosti/app"
	"novosti/app/storage"

	"github.com/revel/revel"
)

// News is the main news app controller.
type News struct {
	*revel.Controller
}

// Share implements the news sharing endpoint.
func (c News) Share() (result revel.Result) {
	title := c.Params.Form.Get("title")
	content := c.Params.Form.Get("content")

	defer func() {
		result = c.Render(title, content)
	}()

	if c.Request.Method != http.MethodPost {
		return
	}

	c.Validation.MinSize(title, 10)
	c.Validation.MaxSize(title, 200)
	c.Validation.MinSize(content, 50)
	c.Validation.MaxSize(content, 1000)

	if c.Validation.HasErrors() {
		return
	}

	storyID, err := app.NewsRepository.CreateStory(storage.NewsStory{
		Title:   title,
		Content: content,
	})
	if err != nil {
		c.Log.Error("unexpected error while creating story in repository", "error", err)
		c.ViewArgs["error"] = revel.Message(c.Request.Locale, "app.error.share")
		return
	}

	c.Log.Info("saved new story", "story_id", storyID)

	if err := app.ReviewQueue.EnqueueReview(c.Request.Context(), string(storyID)); err != nil {
		c.Log.Error("unexpected error while enqueuing story review", "error", err, "story_id", storyID)
		c.ViewArgs["error"] = revel.Message(c.Request.Locale, "app.error.share")
		return
	}

	c.ViewArgs["submitted"] = "t"
	return
}
